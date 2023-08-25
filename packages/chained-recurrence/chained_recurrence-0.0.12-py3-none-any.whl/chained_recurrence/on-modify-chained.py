#!/usr/bin/env python

import os
import sys
from datetime import datetime, time
from time import sleep

import psutil
from tasklib import Task, TaskWarrior


class ChainedTask(Task):
    @classmethod
    def create_link(cls, origin_task):
        """
        Creates a subsequent task based on `origin_task`.
        """
        excluded = Task.read_only_fields + ['start', 'end', 'annotations']
        data = {
            key: origin_task._data[key]
            for key in origin_task._data
            if key not in excluded
        } | {'chainedPrev': origin_task.uuid}

        if (due := origin_task.date_field('due')) is not None:
            data['due'] = due

        if (wait := origin_task.date_field('wait')) is not None:
            data['wait'] = wait
            data['status'] = 'waiting'
        else:
            data['status'] = 'pending'

        task = cls(origin_task.backend, **data)
        task.save()

        origin_task._data['chainedNext'] = task.uuid
        origin_task.read_only_fields = Task.read_only_fields + ['annotations']
        origin_task.save()

        return task

    @property
    def is_chained(self):
        return self._data.get('chained', 'off') == 'on'

    @property
    def status_changed(self):
        return self._data['status'] != self._original_data['status']

    @property
    def uuid(self):
        if 'uuid' in self._data:
            return self._data['uuid'].split('-', 1)[0]

    def date_field(self, field):
        if field in self._data:
            return self.snap_to_day(
                datetime.now(), self._data['entry'], self._data[field]
            )

    def snap_to_day(self, base, entry, field):
        """
        Returns a date that's "snapped" to a day boundary.
        """
        if (ftime := time(field.hour, field.minute)) in [time(0, 0), time(23, 59)]:
            return datetime.combine(
                base.date() + (field.date() - entry.date()),
                ftime,
            )
        else:
            return base + (field - entry)


def process_initial_task(tw):
    """
    Performs the initial modification.
    """
    task = ChainedTask.from_input(backend=tw)
    print(task.export_data(), flush=True)
    return task


def wait_taskwarrior():
    """
    Waits for Taskwarrior to exit, so we're free to modify `.data` files.
    """
    process = psutil.Process().parent()

    if os.fork() != 0:
        sys.exit()

    os.close(1)

    try:
        # Taskwarrior-tui friendly: https://github.com/kdheepak/taskwarrior-tui/issues/513
        while process.status() not in ('terminated', 'zombie'):
            sleep(0.1)
    except psutil.NoSuchProcess:
        return


def main():
    tw = TaskWarrior()
    tw.overrides |= {'default.project': '', 'hooks': 'no', 'recurrence': 'no'}

    task = process_initial_task(tw)

    if task.status_changed and task.completed and task.is_chained:
        print('Creating new chained task.', flush=True)
        wait_taskwarrior()
        ChainedTask.create_link(task)


if __name__ == '__main__':
    main()

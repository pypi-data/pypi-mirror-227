# Taskwarrior Chained Recurrence Hook

Painlessly adds chained recurrence to Taskwarrior. Requires `Python >= 3.8`.

![recurring task illustration](illustration.svg)

In the illustration above, task `26ccff69` is automatically created when task
`90e414dl` is completed. With the new task having the equivalent `due` and
`wait` attributes, relative to it's own `entry` attribute.

It's common to have `due` or `wait` fall on a *day boundary* such as `23:59` or
`00:00`, this is usually because a named date such as `eod` or `sod` was used
when creating the original task. If this is the case, new tasks will be created
with the `due` and `wait` attributes automatically falling on the equivalent
day boundaries. If this sounds convoluted, the "[Usage](#usage)" section below
has a simple example.

## Install

```bash
$ pip install chained-recurrence
$ chained-recurrence install
```


## Usage

Create tasks as you usually would, adding `chained:on`:

```bash
$ task add chained:on 'hair cut'
```

When this task's status is changed to `complete`, a new one will be created.

The `wait` and `due` attributes can also be used, their date and time values
will be updated in relation to the current date and time:

```console
$ date
Mon  1 Jan 18:00:00 GMT 2024

$ task add chained:on wait:1d 'workout'
Created task 1.

$ date
Sat 20 Jan 09:00:00 GMT 2024

$ task 1 done
Completed task ab566e0f 'workout'.
Completed 1 task.
Creating new chained task.
```

The newly created chained task will have the following:

| Attribute | Value               |
| --------- | ------------------- |
| wait      | 2024-01-21 09:00:00 |

### Named Dates

```console
$ date
Mon  1 Jan 18:00:00 GMT 2024

$ task add chained:on wait:sod+1d due:eod+2d 'workout'
Created task 1.

$ date
Sat 20 Jan 09:00:00 GMT 2024

$ task 1 done
Completed task ab566e0f 'workout'.
Completed 1 task.
Creating new chained task.
```
The newly created chained task will have the following:

| Attribute | Value               |
| --------- | ------------------- |
| wait      | 2024-01-21 00:00:00 |
| due       | 2024-01-22 23:59:59 |


## Uninstall

```bash
$ chained-recurrence uninstall
$ pip uninstall chained-recurrence
```

# Bitbucket Pipelines Pipe: Slack Notify on Fail

Sends a custom notification to [Slack](https://slack.com) in after script on non-zero BITBUCKET_EXIT_CODE.

You can configure [Slack integration](https://confluence.atlassian.com/bitbucket/bitbucket-cloud-for-slack-945096776.html) for your repository to get notifications on standard events, such as build failures and deployments. Use this pipe to send your own additional notifications at any point in your pipelines.

## YAML Definition

Add the following snippet to the script section of your `bitbucket-pipelines.yml` file:

```yaml
- pipe: rhendricksen/slack-notify-on-fail:1.0.0
  variables:
    WEBHOOK_URL: '<string>'
    MESSAGE: '<string>'
    # DEBUG: '<boolean>' # Optional.
```

## Variables

| Variable           | Usage                                                       |
| --------------------- | ----------------------------------------------------------- |
| WEBHOOK_URL (*) | Incoming Webhook URL. It is recommended to use a secure repository variable.  |
| MESSAGE (*)     | Notification message. |
| DEBUG           | Turn on extra debug information. Default: `false`. | 

_(*) = required variable._

## Prerequisites

To send notifications to Slack, you need an Incoming Webhook URL. You can follow the instructions [here](https://api.slack.com/incoming-webhooks) to create one.

## Examples

Basic example:

```yaml
script:
  - pipe: rhendricksen/slack-notify:1.0.0
    variables:
      WEBHOOK_URL: $WEBHOOK_URL
      MESSAGE: 'Hello, world!'
```

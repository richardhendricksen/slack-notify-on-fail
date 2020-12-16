import requests
from bitbucket_pipes_toolkit import Pipe, yaml, get_variable


# global variables
SLACK_APP_DEFAULT_COLOR = "#439FE0"
REQUESTS_DEFAULT_TIMEOUT = 10
BASE_SUCCESS_MESSAGE = "Notification successful"
BASE_FAILED_MESSAGE = "Notification failed"


# defines the schema for pipe variables
schema = {
  "WEBHOOK_URL": {
    "type": "string",
    "required": True
  },
  "MESSAGE": {
    "type": "string",
    "required": True
  },
  "DEBUG": {
    "type": "boolean",
    "default": False
  }
}


class SlackNotifyPipe(Pipe):
  def run(self):
    super().run()

    webhook_url = self.get_variable("WEBHOOK_URL")
    message = self.get_variable("MESSAGE")
    debug = self.get_variable("DEBUG")

    # get pipelines specific variables
    workspace = get_variable('BITBUCKET_WORKSPACE', default='local')
    repo = get_variable('BITBUCKET_REPO_SLUG', default='local')
    build = get_variable('BITBUCKET_BUILD_NUMBER', default='local')
    exit_code = get_variable("BITBUCKET_EXIT_CODE", default='local')

    self.log_info(exit_code)
    if exit_code == 0:
      self.log_info("BITBUCKET_EXIT_CODE = 0, skipping sending notification to Slack...")
    else:
      if debug:
        self.log_info("Enabling debug mode.")
      self.log_info("Sending notification to Slack...")

      headers = {'Content-Type': 'application/json'}
      pretext = f"Notification sent from <https://bitbucket.org/{workspace}/{repo}/addon/pipelines/home#!/results/{build}|Pipeline #{build}>"

      payload = {
        "attachments": [
          {
            "fallback": message,
            "color": SLACK_APP_DEFAULT_COLOR,
            "pretext": pretext,
            "text": message,
            "mrkdwn_in": ["pretext"]
          }
        ]
      }

      try:
        response = requests.post(
          url=webhook_url,
          headers=headers,
          json=payload,
          timeout=REQUESTS_DEFAULT_TIMEOUT
        )
      except requests.exceptions.Timeout as error:
        message = self.create_message(
          BASE_FAILED_MESSAGE,
          'Request to Slack timed out',
          error
        )
        self.fail(message)
      except requests.ConnectionError as error:
        message = self.create_message(
          BASE_FAILED_MESSAGE,
          'Connection Error',
          error
        )
        self.fail(message)

      self.log_info(f"HTTP Response: {response.text}")

      # https://api.slack.com/messaging/webhooks
      if 200 <= response.status_code <= 299:
        self.success(BASE_SUCCESS_MESSAGE)
      else:
        self.fail(BASE_FAILED_MESSAGE)

  def create_message(self, base_message, error_message, error_text):
    message = '{}: {}{}'.format(
      base_message,
      error_message,
      f': {error_text}' if self.get_variable("DEBUG") else f'.'
    )
    return message


if __name__ == '__main__':
  with open('/pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  pipe = SlackNotifyPipe(schema=schema, pipe_metadata=metadata, check_for_newer_version=True)
  pipe.run()

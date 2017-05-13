#!/usr/bin/env python
import os
import sys
# import newrelic.agent
# newrelic.agent.initialize()

# print("Newrelic init")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "structchat.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

import boto3
import os
import requests
import datetime

# define environment variables
MEETUP_API_KEY = os.environ["MEETUP_API_KEY"]
TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def run_query(
    query,
):  # A simple function to use requests.post to make the API call. Note the json= section.
    """
    Purpose:
        Run the graphql query
    Args:
        queryL the meetup graphql query
    Returns:
        N/A
    """
    headers = {"Authorization": "Bearer " + MEETUP_API_KEY}
    request = requests.post(
        "https://api.meetup.com/gql", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()
    else:
        print("Failed request: " + str(request))
        print(query)
        return


def gen_query(meetup_id):
    """
    Purpose:
        Create meetup graphql query
    Args:
        meetup_id: current meetup
    Returns:
        graphql query
    """

    meetup_query = (
        """
    {
    groupByUrlname(urlname: \""""
        + meetup_id
        + """\") {
    name
    city
    link
    state
    country
    description
    memberships {
      count
    }
    upcomingEvents(input: {first: 3}) {
      count
      edges {
        node {
          id
          title
          dateTime
          eventUrl
          going
          isOnline
        }
      }
    }
    pastEvents(input: {first: 1}) {
      count
    }
  }
}

"""
    )

    return meetup_query


def handler(event, context):
    # List of meetup groups
    meetup_groups = [
        "amazon-web-services-dmv",
        "the-boston-amazon-web-services-meetup-group",
        "AWS-NYC",
    ]

    time_now = datetime.datetime.now()
    collected_time = time_now.strftime("%m/%d/%Y")

    # Go through list and run graphql query
    for currentgroup in meetup_groups:
        print(f"Current group: {currentgroup}")
        curr_query = gen_query(currentgroup)
        meetup_raw = run_query(curr_query)

        meetup_json = meetup_raw["data"]["groupByUrlname"]

        if not meetup_json:
            continue

        # Create meetup json
        meetup_json_vals = {}
        meetup_json_vals["state"] = meetup_json["state"]
        meetup_json_vals["meetup_link"] = meetup_json["link"]
        meetup_json_vals["meetup_name"] = meetup_json["name"]
        meetup_json_vals["num_members"] = meetup_json["memberships"]["count"]
        meetup_json_vals["city"] = meetup_json["city"]
        meetup_json_vals["country"] = meetup_json["country"]
        meetup_json_vals["collected_date"] = collected_time
        meetup_json_vals["num_past_events"] = meetup_json["pastEvents"]["count"]
        meetup_json_vals["num_upcoming_events"] = meetup_json["upcomingEvents"]["count"]

        # Check upcoming meetups
        upcoming_event_list = []
        upcoming_rsvps = 0
        if meetup_json["upcomingEvents"]["count"] > 0:
            for meetup_event in meetup_json["upcomingEvents"]["edges"]:
                event_name = meetup_event["node"]["title"]
                num_going = meetup_event["node"]["going"]

                upcoming_event_list.append(event_name)
                upcoming_rsvps += num_going

        meetup_json_vals["upcoming_events_list"] = upcoming_event_list
        meetup_json_vals["number_of_rsvps"] = upcoming_rsvps

        # Add data to DynamoDB
        table.put_item(Item={"id": currentgroup, "map": meetup_json_vals})

        # Print results
        print(meetup_json_vals)

    print("Done and done")
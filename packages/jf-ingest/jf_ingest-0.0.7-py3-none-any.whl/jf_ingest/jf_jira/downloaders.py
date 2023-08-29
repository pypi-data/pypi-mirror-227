from jira import JIRA
# jira renamed this between api versions for some reason
try:
    from jira.resources import AgileResource as AGILE_BASE_REST_PATH
except ImportError:
    from jira.resources import GreenHopperResource as AGILE_BASE_REST_PATH


def get_jira_connection(config, creds, max_retries=3):
    kwargs = {
        'server': config.jira_url,
        'max_retries': max_retries,
        'options': {
            'agile_rest_path': AGILE_BASE_REST_PATH,
            'verify': not config.skip_ssl_verification,
        },
    }

    if creds.jira_username and creds.jira_password:
        kwargs['basic_auth'] = (creds.jira_username, creds.jira_password)
    elif creds.jira_bearer_token:
        kwargs['options']['headers'] = {
            'Authorization': f'Bearer {creds.jira_bearer_token}',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Atlassian-Token': 'no-check',
        }
    else:
        raise RuntimeError(
            'No valid Jira credentials found! Check your JIRA_USERNAME, JIRA_PASSWORD, or JIRA_BEARER_TOKEN environment variables.'
        )

    jira_connection = JIRA(**kwargs)

    jira_connection._session.headers[
        'User-Agent'
    ] = f'jellyfish/1.0 ({jira_connection._session.headers["User-Agent"]})'

    return jira_connection


def download_fields(jira_connection: JIRA, include_fields=[], exclude_fields=[]):
    print('downloading jira fields... ', end='', flush=True)

    filters = []
    if include_fields:
        filters.append(lambda field: field['id'] in include_fields)
    if exclude_fields:
        filters.append(lambda field: field['id'] not in exclude_fields)

    fields = [field for field in jira_connection.fields() if all(filter(field) for filter in filters)]

    print('✓')
    return fields

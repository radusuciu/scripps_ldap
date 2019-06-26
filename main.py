from exceptions import UserNotFoundInLDAP
import ldap3
import config
import click

server = ldap3.Server(config.LDAP_URI, connect_timeout=1)

ldap_con = ldap3.Connection(
    server,
    user=config.LDAP_BIND_DN,
    password=config.LDAP_BIND_PASSWORD,
    receive_timeout=True
)

ldap_con.bind()

def query_ldap_user(identifier):
    """Get information about a user throught AD."""
    result = ldap_con.search(
        search_base=config.LDAP_BASE_DN,
        search_filter=config.LDAP_SEARCH_FILTER.format(identifier),
        search_scope=ldap3.SUBTREE,
        attributes=ldap3.ALL_ATTRIBUTES
    )

    data = ldap_con.entries

    if result and data:
        return data[0]
    else:
        raise UserNotFoundInLDAP


def get_first_and_last_name(identifier):
    """Get first and last name from AD."""
    try:
        user = query_ldap_user(identifier)
        return user.givenName.value, user.sn.value
    except UserNotFoundInLDAP:
        return ('', '')

@click.command()
@click.argument('username', nargs=-1)
def names(username):
    for name in username:
        click.echo('\t'.join(get_first_and_last_name(name)))
    ldap_con.unbind()

if __name__ == '__main__':
    names()

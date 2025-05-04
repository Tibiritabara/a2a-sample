from hosts.multiagent.host_agent import HostAgent
from pydantic import HttpUrl


def main(remote_hosts: list[HttpUrl]):
    root_agent = HostAgent(
        remote_agent_addresses=[str(remote_host) for remote_host in remote_hosts]
    ).create_agent()
    root_agent.


if __name__ == "__main__":
    main([HttpUrl("http://localhost:10000")])

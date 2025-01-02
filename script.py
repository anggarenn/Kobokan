import json
import os
import sys





def create_grass_compose(i, ip_address, user_email, user_password):
    http_api_port = 2002 + i
    p2p_tcp_port = 3002 + i
    p2p_ws_port = 4002 + i
    typesense_port = 1180 + i
    docker_compose_template = f"""
version: "3.9"
services:
  grass-node{i}:
    container_name: grass-node{i}
    hostname: my_device
    image: mrcolorrain/grass-node
    restart: on-failure
    environment:
      USER_EMAIL: {user_email}
      USER_PASSWORD: {user_password}
    ports:
      - "{590+i}:{590+i}"
      - "{608+i}:{608+i}"
"""
    save_docker_compose_file(docker_compose_template, i + 1)
    print(f"Generated docker-compose{i + 1}.yaml for grass-node{i}")


def save_docker_compose_file(content, i):
    filename = f'docker-compose{i}.yaml'
    with open(filename, 'w') as file:
        file.write(content)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <ip_address> <num_nodes>")
        sys.exit(1)

    ip_address = sys.argv[1]
    num_nodes = int(sys.argv[2])

    # Load user-pass data from userpass.json
    with open("userpass.json", "r") as json_file:
        userpass_data = json.load(json_file)

    # Ensure enough entries are available for the number of nodes
    if len(userpass_data) < num_nodes:
        print("Error: Not enough USER_EMAIL and USER_PASSWORD entries in userpass.json")
        sys.exit(1)

    for i in range(num_nodes):
        user_email = userpass_data[i]["USER_EMAIL"]
        user_password = userpass_data[i]["USER_PASSWORD"]
        create_grass_compose(i, ip_address, user_email, user_password)


if __name__ == "__main__":
    main()
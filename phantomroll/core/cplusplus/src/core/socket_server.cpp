#include "core/socket_server.hpp"
#include <iostream>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <cstring>

SocketServer::SocketServer(int port) : port_(port), running_(false), server_fd_(-1) {}

SocketServer::~SocketServer() {
    stop();
}

void SocketServer::start() {
    running_ = true;
    server_thread_ = std::thread(&SocketServer::run, this);
}

void SocketServer::stop() {
    running_ = false;
    if (server_fd_ != -1) close(server_fd_);
    if (server_thread_.joinable()) server_thread_.join();
}

void SocketServer::run() {
    server_fd_ = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd_ == 0) {
        std::cerr << "[SocketServer] Failed to create socket\n";
        return;
    }

    sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port_);

    if (bind(server_fd_, (struct sockaddr*)&address, sizeof(address)) < 0) {
        std::cerr << "[SocketServer] Bind failed\n";
        return;
    }

    if (listen(server_fd_, 3) < 0) {
        std::cerr << "[SocketServer] Listen failed\n";
        return;
    }

    std::cout << "[SocketServer] Listening on port " << port_ << std::endl;

    while (running_) {
        socklen_t addrlen = sizeof(address);
        int client_socket = accept(server_fd_, (struct sockaddr*)&address, &addrlen);
        if (client_socket >= 0) {
            std::thread(&SocketServer::handle_client, this, client_socket).detach();
        }
    }
}

void SocketServer::handle_client(int client_socket) {
    char buffer[1024] = {0};
    ssize_t bytes_read = read(client_socket, buffer, 1024);

    if (bytes_read > 0) {
        std::string command(buffer, bytes_read);
        std::cout << "[SocketServer] Command received: " << command << std::endl;

        // TODO: route command to core logic
        std::string response = "ack: " + command;
        send(client_socket, response.c_str(), response.size(), 0);
    }

    close(client_socket);
}

#ifndef SOCKET_SERVER_HPP
#define SOCKET_SERVER_HPP

#include <string>
#include <thread>
#include <atomic>

class SocketServer {
public:
    SocketServer(int port);
    ~SocketServer();

    void start();
    void stop();

private:
    int server_fd_;
    int port_;
    std::atomic<bool> running_;
    std::thread server_thread_;

    void run();
    void handle_client(int client_socket);
};

#endif // SOCKET_SERVER_HPP

#define _GNU_SOURCE  
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <limits.h>
#include <pthread.h>
#include <sys/un.h>
#include "server.h"

#define SOCKET_NAME "unix_sock"
#define ERROR_OPENING_FILE -1
#define BUFFER_SIZE 256

int main(int argc, char* argv[])
{    
    
    struct sockaddr_un sock;
    int ret;
    int data_socket;   
    char buffer[BUFFER_SIZE];    

    unlink(SOCKET_NAME);

    int connection_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (connection_socket == -1)
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    printf("Master socket created!\n");

    /* Initialization */
    memset(&sock, 0, sizeof(struct sockaddr_un));

    /* Specify the socket credentials */
    sock.sun_family = AF_UNIX;
    strncpy(sock.sun_path, SOCKET_NAME, sizeof(sock.sun_path) - 1);

    /* Bind socket to socket name */ 
    ret = bind(connection_socket, (const struct sockaddr*) &sock, sizeof(struct sockaddr_un));  
    if (ret == -1) 
    {
        perror("bind");
        exit(EXIT_FAILURE);
    }    
    printf("bind() call succeed\n");

    /* Prepare for accepting connections */
    ret = listen(connection_socket, 20);
    if (ret == -1)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }  

    /* Wait for incoming connection */
    printf("Waiting on accept() sys call\n");

    data_socket = accept(connection_socket, NULL, NULL);

    if (data_socket == -1) 
    {
        perror("accept");
        exit(EXIT_FAILURE);
    }
    
    printf("Connection accepted from client\n");      

    while (true)
    {
        last_idx = 0;
        
        /* Prepare the buffer to recv the data */
        memset(buffer, 0, BUFFER_SIZE);            
                
        /* Wait for next data packet */
        /* Server is blocked here. Waiting for the data to arrive from client, 'read' is a blocking system call */
            
        printf("Waiting for expected length of data from the client\n");
        int expectedLength = 0;
        int bytes_read = read(data_socket, &expectedLength, sizeof(expectedLength));
        if (bytes_read == -1)
        {
            perror("read 1");
            exit(EXIT_FAILURE);
        } 

        if (expectedLength == 0)
        {
            printf("Receive 0 length terminating\n");
            break;
        }

        bytes_read = 0;
        while (bytes_read < expectedLength)
        {
            ret = read(data_socket, buffer + bytes_read, BUFFER_SIZE - bytes_read);
            if (ret == -1)
            {
                perror("read 2");
                exit(EXIT_FAILURE);
            } 
            bytes_read += ret;
        }

        printf("Client has send: %s\n", buffer);          
        
        int num = 0;
        for(int i=0; i<bytes_read; i++)       
        {
            if(buffer[i] == ';')
            {            
                num++; 
                func_copy_from_buffer(i, num, buffer);                     
            }        
        }

        open_file();        
        create_filter_info();     
        create_action_info();
        for (int i = 0; i < NUM_OF_ENUMS; i++)
        {
            create_service(i);
        } 
        close_file();

        /* After creating service configuration file send it to python */           
        
        int fd = open("export_service.txt", O_RDONLY);
        if (fd < 0)
        {
            printf("Error while opening file for riding!\n");
            return ERR_NUM;
        }   
        char* temp = read_file_in_buff(fd,"export_service.txt");        

        printf("Sending service configuration...%s\n", temp);
        int payload_length = strlen(temp);
        /* Send first the integer containing the length of the data */
        write(data_socket, &payload_length, sizeof(int));
        /* Send the actual data. */
        write(data_socket, temp, strlen(temp));       

        /* Execute shell script that imports service configuration to ftp server */
        int pid = fork();
        char* arg = NULL;
        if(pid == 0)             
            execv("./ftp.sh", &arg);        
    }    
    
    /* Close socket */
    close(data_socket);
    
    /* Close the master socket */
    close(connection_socket);
    printf("Connection closed..\n");
    
    /* Server should release resources before getting terminated. Unlink the socket */    
    unlink(SOCKET_NAME);    
    exit(EXIT_SUCCESS);
}
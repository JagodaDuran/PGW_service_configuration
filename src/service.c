#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/types.h>
#include "server.h"

/************************ MACRO DEFINITIONS **************************/

#define ERROR_EXIT(exit_code, message) \
    ({fprintf(stderr, "%s\nError at line %d in function %s\n",\
        message, __LINE__, __func__);\
    exit(exit_code); })

/************************ STATIC VARIABLE DEFINITIONS ****************/

static FILE *fp;
static service service1;

/************************ GLOBAL VARIABLE DEFINITION *****************/

int last_idx = 0;

/************************ GLOBAL FUNCTION DEFINITIONS ****************/ 

void open_file(void)
{
    fp = fopen("export_service.txt", "w");
    if (fp == NULL)
    {
        ERROR_EXIT(-1, "Error while opening file for writing\n");
    }
}

void close_file(void)
{
    if(fp != 0)
        fclose(fp);
}

char *read_file_in_buff(int fd, char *file_name)
{
    struct stat file_info;
    if (stat(file_name, &file_info) < 0)
    {
        printf("Error while retrieving information from file!\n");
    }
    long int file_size = file_info.st_size;
    char *buff = malloc(file_size * sizeof(char) + 1);

    unsigned long long bytes_read = 0;
    unsigned long long total_bytes_read = 0;

    while ((bytes_read = read(fd, buff + total_bytes_read, file_size)) > 0)
        total_bytes_read += bytes_read;

    buff[file_size] = 0;
    return buff;
}

void func_copy_from_buffer(int i, int num, char *buffer)
{
    switch (num)
    {
    case 1:
        memcpy(service1.service_name, buffer + last_idx, i - last_idx);
        printf("Service name: %s\n", service1.service_name);
        break;
    case 2:
        memcpy(service1.monitoring_key, buffer + last_idx, i - last_idx);
        printf("Monitoring key: %s\n", service1.monitoring_key);
        break;
    case 3:
        memcpy(service1.priority_n, buffer + last_idx, i - last_idx);
        printf("Priority of normal rule: %s\n", service1.priority_n);
        break;
    case 4:
        memcpy(service1.priority_e, buffer + last_idx, i - last_idx);
        printf("Priority of exhaust rule: %s\n", service1.priority_e);
        break;
    case 5:
        memcpy(service1.rg_n, buffer + last_idx, i - last_idx);
        printf("Rating group for normal rule: %s\n", service1.rg_n);
        break;
    case 6:
        memcpy(service1.rg_e, buffer + last_idx, i - last_idx);
        printf("Rating group for exhaust rule: %s\n", service1.rg_e);
        break;
    case 7:
        memcpy(service1.speed_n_dw, buffer + last_idx, i - last_idx);
        printf("Downlink speed for normal rule: %s\n", service1.speed_n_dw);
        break;
    case 8:
        memcpy(service1.speed_n_up, buffer + last_idx, i - last_idx);
        printf("Uplink speed for normal rule: %s\n", service1.speed_n_up);
        break;
    case 9:
        memcpy(service1.speed_e_dw, buffer + last_idx, i - last_idx);
        printf("Downlink speed for exhaust rule: %s\n", service1.speed_e_dw);
        break;
    case 10:
        memcpy(service1.speed_e_up, buffer + last_idx, i - last_idx);
        printf("Uplink speed for exhaust rule: %s\n", service1.speed_e_up);
        break;
    case 11:
        service1.service_filter = buffer[last_idx] - '0';
        if (service1.service_filter == 5)
        {
            memcpy(service1.filter_ip_server, buffer + last_idx + 1, i - last_idx - 1);
            printf("Ip address is %s\n", service1.filter_ip_server);
        }
        if (service1.service_filter == 6)
        {
            memcpy(service1.filter_domain_name, buffer + last_idx + 1, i - last_idx - 1);
            printf("Ip address is %s\n", service1.filter_domain_name);
        }
        printf("Selected filter: %d\n", service1.service_filter);
        break;
    case 12:
        service1.service_action = buffer[last_idx] - '0';
        printf("Selected action: %d\n", service1.service_action);
        break;
    default:
        break;
    }
    last_idx = i + 1;
}

void create_filter_info(void)
{
    int err;
    char *msg;

    switch (service1.service_filter)
    {
        case 1:
            service1.filter = "fg_any";    
            err = asprintf(&msg, "filter-group fg_any filter f_any\nfilter f_any l34-protocol any\n");
            break;
        case 2:
            service1.filter = "fg_tcp";    
            err = asprintf(&msg, "filter-group fg_tcp filter f_tcp\nfilter f_tcp l34-protocol tcp\n");
            break;
        case 3:
            service1.filter = "fg_udp";    
            err = asprintf(&msg, "filter-group fg_udp filter f_udp\nfilter f_udp l34-protocol udp\n");
            break;
        case 4:
            service1.filter = "fg_dns"; 
            err = asprintf(&msg, "filter-group fg_dns filter dns\nfilter dns l34-protocol any server-ip 88.99.68.1 32 server-port eq 53\n");
            break;
        case 5:
            service1.filter = "fg_ip";    
            err = asprintf(&msg, "filter-group fg_ip filter filter_ip\nfilter filter_ip l34-protocol any server-ip %s 32\n", service1.filter_ip_server);
            break;
        case 6:
            service1.filter = "fg_host_name";    
            err = asprintf(&msg, "host host_name domain *.%s sequence 65535\nfilter filter_host_name l34-protocol any host host_name\nfilter-group fg_host_name filter filter_host_name\nl7-info l7i_host_name url *.%s*/* referer-correlation enable l7-category-group cg_host_name\nl7-info-group l7g_host_name l7-info l7i_host_name sequence 45001\n", service1.filter_domain_name, service1.filter_domain_name);
            break;
        default:
            break;
    }

    if (err == -1)
    {
        ERROR_EXIT(-1, "Error while executing the function asprintf!\n");
    }  

    err = fputs(msg, fp);
    if (err == EOF)
    {
        ERROR_EXIT(-1, "Error while executing the function fputs");
    }
   
    free(msg); 
}

void create_action_info(void)
{
    int err;
    char *msg; 

    switch (service1.service_action)
    {
        case 1:
            service1.action = "ap_rg";
            err = asprintf(&msg, "action-list al_rg charge-point\naction-property ap_rg up-initial up-action-list al_rg down-action-list al_rg\n");
            break;
        case 2:            
            service1.action = "ap_he";
            err = asprintf(&msg, "action-list al_he charge-point header-enrichment header_msisdn_he\naction-property ap_he up-initial up-action-list al_he down-action-list al_he\nrule-enrichment rule rule_he header-enrichment enable\n");
            break;
        case 3:            
            service1.action = "ap_discard";
            asprintf(&msg, "action-list al_discard gate discard charge-point\naction-property ap_discard up-initial up-action-list al_discard down-action-list al_discard down-initial up-action-list al_discard down-action-list al_discard\n");
            break;
        default:
            break;
    }
    
    if (err == -1)
    {
        ERROR_EXIT(-1, "Error while executing the function asprintf!\n");
    }    

    err = fputs(msg, fp);
    if (err == EOF)
    {
        ERROR_EXIT(-1, "Error while executing the function fputs");
    }
   
    free(msg);    
}

void create_service(e_type id)
{
    int err;
    char *msg;   

    switch (id)
    {        
        case RG_NORMAL:
            err = asprintf(&msg, "cbb-id rg%s_off charge-method offline rg %s metering volume\ncbb-id rg%s_on charge-method online rg %s metering volume\ncharge-property cp_rg%s up-initial offline rg%s_off online rg%s_on down-initial offline rg%s_off online rg%s_on\n", service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n, service1.rg_n);
            break;
        case RG_EXHAUST:
            err = asprintf(&msg, "cbb-id rg%s_off charge-method offline rg %s metering volume\ncbb-id rg%s_on charge-method online rg %s metering volume\ncharge-property cp_rg%s up-initial offline rg%s_off online rg%s_on down-initial offline rg%s_off online rg%s_on\n", service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e, service1.rg_e);
            break;
        case BMW_RULE_NORMAL:
            err = asprintf(&msg, "bwm-controller bc_%sm car cir 21600 cbs 4050000 pir 43200 pbs 8100000 green pass yellow drop red drop\nbwm-service bs_dl%sm_ul%sm category-property cp_dl%sm_ul%sm\nbwm-rule br_dl%sm_ul%sm bwm-service bs_dl%sm_ul%sm subscriber uplink bc_%sm downlink bc_%sm priority 50\n", service1.speed_n_dw, service1.speed_n_dw, service1.speed_n_up, service1.speed_n_dw, service1.speed_n_up, service1.speed_n_dw, service1.speed_n_up, service1.speed_n_dw, service1.speed_n_up, service1.speed_n_dw, service1.speed_n_up);
            break;
        case BMW_RULE_EXHAUST:
            err = asprintf(&msg, "bwm-controller bc_%sk car cir %s cbs 24000 pir 256 pbs 48000 green pass yellow drop red drop\nbwm-service bs_dl%s_ul%sk category-property cp_dl%sk_ul%sk\nbwm-rule br_dl%sk_ul%sk bwm-service bs_dl%sk_ul%sk subscriber uplink bc_%sk downlink bc_%sk priority 50\n", service1.speed_e_dw, service1.speed_e_dw, service1.speed_e_dw, service1.speed_e_up, service1.speed_e_dw, service1.speed_e_up, service1.speed_e_dw, service1.speed_e_up, service1.speed_e_dw, service1.speed_e_up, service1.speed_e_dw, service1.speed_e_up);
            break;
        case CATEGORY_PROPERTY_NORMAL:
            err = asprintf(&msg, "category-property cp_dl%sm_ul%sm\n", service1.speed_n_dw, service1.speed_n_up);
            break;
        case CATEGORY_PROPERTY_EXHAUST:
            err = asprintf(&msg, "category-property cp_dl%sk_ul%sk\n", service1.speed_e_dw, service1.speed_e_up);
            break;
        case CATEGORY_GROUP_NORMAL:
            err = asprintf(&msg, "category-group cg_%s_normal category-property cp_dl%sm_ul%sm charge-property cp_rg%s action-property %s monitoring-key %s\n", service1.service_name, service1.speed_n_up, service1.speed_n_dw, service1.rg_n, service1.action, service1.monitoring_key);
            break;
        case CATEGORY_GROUP_EXHAUST:
            err = asprintf(&msg, "category-group cg_%s_exhaust category-property cp_dl%sk_ul%sk charge-property cp_rg%s action-property %s monitoring-key %s\n", service1.service_name, service1.speed_e_up, service1.speed_e_dw, service1.rg_e, service1.action, service1.monitoring_key);
            break;
        case RULE_NORMAL:
            err = asprintf(&msg, "rule rule_%s_normal filter-group %s service-category-group cg_%s_normal priority %s\n", service1.service_name, service1.filter, service1.service_name, service1.priority_n);
            break;
        case RULE_EXHAUST:
            err = asprintf(&msg, "rule rule_%s_exhaust filter-group %s service-category-group cg_%s_normal priority %s\n", service1.service_name, service1.filter, service1.service_name, service1.priority_e);
            break;
        case USER_PROFILE:
            err = asprintf(&msg, "user-profile up_%s_normal\nrule-binding rule_%s_normal priority 1010\nddos-check disable\nquota-application-action buffer\nuser-profile up_%s_exhaust\nrule-binding rule_%s_exhaust priority 1010\nddos-check disable\nquota-application-action buffer\n", service1.service_name, service1.service_name, service1.service_name, service1.service_name);
            break;        
        default:
            ERROR_EXIT(-1, "Incorrect enum type!\n");
            break;
    }
    
    if (err == -1)
    {
        ERROR_EXIT(-1, "Error while executing the function asprintf!\n");
    }  

    err = fputs(msg, fp);
    if (err == EOF)
    {
        ERROR_EXIT(-1, "Error while executing the function fputs");
    }
   
    free(msg);    
}




#ifndef service_H
#define service_H
#include <stdio.h>
#include <stdbool.h>
#define ERR_NUM -1

#define MAX_CHAR 30

typedef struct service
{
    char service_name[MAX_CHAR];        
    char monitoring_key[MAX_CHAR]; 
    char priority_n[MAX_CHAR];  
    char priority_e[MAX_CHAR];  
    char rg_n[MAX_CHAR];
    char rg_e[MAX_CHAR];
    char speed_n_dw[MAX_CHAR];
    char speed_n_up[MAX_CHAR];
    char speed_e_dw[MAX_CHAR];
    char speed_e_up[MAX_CHAR];    
    char charge_property_n[MAX_CHAR];
    char charge_property_e[MAX_CHAR];
    char category_property_n[MAX_CHAR];
    char category_property_e[MAX_CHAR];
    int service_action;
    char* action; 
    int service_filter;
    char* filter;
    char filter_ip_server[MAX_CHAR];
    char filter_domain_name[MAX_CHAR];   

} service;

typedef enum type
{    
    RG_NORMAL,
    RG_EXHAUST,
    BMW_RULE_NORMAL,
    BMW_RULE_EXHAUST,
    CATEGORY_PROPERTY_NORMAL,
    CATEGORY_PROPERTY_EXHAUST,
    CATEGORY_GROUP_NORMAL,
    CATEGORY_GROUP_EXHAUST,
    RULE_NORMAL,
    RULE_EXHAUST,
    USER_PROFILE,
    NUM_OF_ENUMS,

} e_type;

extern int last_idx;
void open_file(void);
void close_file(void);
void func_copy_from_buffer(int i, int num, char* buffer);
char* read_file_in_buff(int fd, char* file_name);
void create_service(e_type id);
void create_action_info(void);
void create_filter_info(void);

#endif
# from django.urls import include


def check_active_sidebar_links(request):
    current_url = f"{request.resolver_match.namespace}:{request.resolver_match.url_name}"

    leave_status = False
    roster_status = False
    employee_status = False
    attendance_status = False
    fiscal_year_status = False


    # checking leave urls active status
    leave_urls =[ 'leave:leave_list', 'leave:leave_type_list']
    if current_url in leave_urls:
        leave_status = True

    # checking roster urls active status
    roster_urls =[ 'roster:shift_list']
    if current_url in roster_urls:
        roster_status = True

    employee_urls =[ 'user:employee_list']
    if current_url in employee_urls:
        employee_status = True
    
    attendance_urls =[ 'attendance:request_list']
    if current_url in attendance_urls:
        attendance_status = True
    
    fiscal_year_urls =[ 'fiscal_year:list']
    if current_url in fiscal_year_urls:
        fiscal_year_status = True


    context = {     
        'current_url': current_url,
        'leave_status': leave_status,
        'roster_status': roster_status,
        'employee_status': employee_status,
        'attendance_status': attendance_status,
        'fiscal_year_status': fiscal_year_status,      
    }
    return context

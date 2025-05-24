# from django.urls import include


def check_active_sidebar_links(request):
    current_url = f"{request.resolver_match.namespace}:{request.resolver_match.url_name}"

    leave_status = False

    # checking leave urls active status
    leave_urls =[ 'leave:leave_list', 'leave:leave_type_list']
    if current_url in leave_urls:
        leave_status = True


    context = {     
        'current_url': current_url,
        'leave_status': leave_status,
        
    }
    return context

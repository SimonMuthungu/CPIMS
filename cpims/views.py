"""Main CPIMS common views."""
import memcache
import sys
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from cpovc_registry.functions import dashboard, ovc_dashboard, get_public_dash_ovc_hiv_status, \
    get_ovc_hiv_status, fetch_locality_data, fetch_total_ovc_ever, fetch_total_ovc_ever_exited, \
    fetch_total_wout_bcert_at_enrol, get_cbo_list, get_ever_tested_for_HIV, _get_ovc_active_hiv_status, \
    _get_ovc_served_stats, fetch_total_w_bcert_2date, fetch_total_s_bcert_aft_enrol, fetch_new_ovcregs_by_period, \
    fetch_exited_hsehlds_by_period, fetch_exited_ovcs_by_period, fetch_served_bcert_by_period, \
    fetch_u5_served_bcert_by_period
from cpovc_main.functions import get_dict
from cpovc_access.functions import access_request
from django.contrib.auth.decorators import login_required
from zeep.helpers import serialize_object


mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def public_dash(request):
    """Some default page for the home page / Dashboard."""
    try:
        print("we are here")
        # vals = get_dashboard(request)
        return render(request, 'public_dash.html')
    except Exception as e:
        print(('dashboard error - %s' % (str(e))))
        raise e


# #################### Dash
def public_dashboard_reg(request):
    try:
        print("we are here")
        # vals = get_dashboard(request)
        # return render(request, 'public_dash_' + p_dash + '.html')
        return render(request, 'public_dash/reg.html')
    except Exception as e:
        print(('dashboard error - %s' % (str(e))))
        raise e
    

def verify_user_by_iprs(request):
    if request.method == 'POST':
        username = request.POST.get('search_name')
        password = request.POST.get('search_criteria')

        print(f'\nusername submitter for login:{username}\nAnd pswd: {password}')

        import json
        from zeep import Client
        from zeep.exceptions import Fault
        from zeep.helpers import serialize_object

        # WSDL service URL
        wsdl_url = 'https://dev.cpims.net/IPRSServerwcf?wsdl'


        def check_wsdl_connection():

            try:
                client = Client(wsdl=wsdl_url)
                print("Connection to WSDL service successful!")
                return client
            except Exception as e:
                print(f"Failed to connect to WSDL service: {e}")
                # return None
            
        try:
            client = check_wsdl_connection()
        except Exception as e:
            print('Exception occured while trying to create client')
            raise ImportWarning
        
        # Logic to verify user credentials (api check)
        def perform_login(client):

            from zeep.exceptions import Fault


            # Create login payload
            login_payload = {
                'log': username,
                'pass': password
            }

            try:
                # login credentials
                response = client.service.Login(**login_payload)  # Modify the method name as per actual WSDL
                print(f'Im likely the culprit, heres what I am: {response}')
                response_dict = serialize_object(response)

                if response_dict.get('LoginSuccess', False):
                    print("Login successful!")

                    # creating a session with the returned token
                    session_token = response_dict.get('SessionToken')
                    request.session['session_token'] = session_token

                    return redirect('passport_page')
                else:
                    print("Invalid credentials, please try again.")
                    return render(request, 'verify_user.html', {'error': 'Verification failed. Please try again.'})

            except Fault as fault:
                print(f"SOAP Fault during login: {fault}")
                return render(request, 'verify_user.html', {'error': 'Verification failed. Please try again.'})

            except Exception as e:
                print(f"An error occurred: {e}")
                return render(request, 'verify_user.html', {'error': 'Verification failed. Please try again.'})
            
        perform_login(client)
 
    return render(request, 'verify_user.html', {'error': 'Verification failed. Please try again.'})

    # return render(request, 'verify_user.html')


def passport_page(request):
    if request.method == 'POST':
        passport_id = request.POST.get('passport_id', '')
        id_number = request.POST.get('id_number', '')
        birth_certificate = request.POST.get('birth_certificate', '')
        birth_certificate_serial = request.POST.get('birth_certificate_serial', '')

        import json
        from zeep import Client
        from zeep.exceptions import Fault
        from zeep.helpers import serialize_object

        # WSDL service URL
        wsdl_url = 'https://dev.cpims.net/IPRSServerwcf?wsdl'


        def check_wsdl_connection():

            try:
                client = Client(wsdl=wsdl_url)
                print("Connection to WSDL service successful!")
                return client
            except Exception as e:
                print(f"Failed to connect to WSDL service: {e}")
                return None
            
        try:
            client = check_wsdl_connection()
        except Exception as e:
            print('Exception occured while trying to create client')
            raise ImportWarning




        # Process each form independently
        if passport_id:
            def get_data_by_id(client, token):

                    input_payload = {
                        'id_number': id_number,
                        'session_token': token  # Assuming session token or similar is needed
                    }

                    try:
                        response = client.service.GetDataByIdCard(**input_payload)
                        response_dict = serialize_object(response)

                        if not response_dict.get('ErrorOccurred', True):
                            print("Person's Data Retrieved Successfully in JSON Format:")
                            print(json.dumps(response_dict, indent=4))

                            return JsonResponse(response_dict, json_dumps_params={'indent': 4})  
                        
                        else:
                            print(f"Error: {response_dict.get('ErrorMessage', 'Unknown error')}")
                            return JsonResponse('Error', json_dumps_params={'indent': 4})

                    except Fault as fault:
                        print(f"SOAP Fault: {fault}")
                    except Exception as e:
                        print(f"An Exception other than Fault occurred: {e}")
                        return HttpResponse(f"Passport ID {passport_id} submitted successfully!")
                    
            session_token = request.session.get('session_token', None)
            get_data_by_id(client, session_token)
                        
        # elif id_number:
        #     return HttpResponse(f"ID Number {id_number} submitted successfully!")
        
        # elif birth_certificate and birth_certificate_serial:
        #     return HttpResponse(f"Birth Certificate {birth_certificate} with Serial {birth_certificate_serial} submitted successfully!")
        
        else:
            return HttpResponse("No data submitted.")
    
    # Render the form if the method is GET or no data was submitted
    return render(request, 'check_details_from_iprs.html')


def public_dashboard_hivstat(request):
    try:
        print("we are here")
        # vals = get_dashboard(request)
        # return render(request, 'public_dash_' + p_dash + '.html')
        return render(request, 'public_dash/hivstat.html')
    except Exception as e:
        print('dashboard error - %s' % (str(e)))
        raise e


def public_dashboard_served(request):
    try:
        print("we are here")
        # vals = get_dashboard(request)
        # return render(request, 'public_dash_' + p_dash + '.html')
        return render(request, 'public_dash/served.html')
    except Exception as e:
        print('dashboard error - %s' % (str(e)))
        raise e


# #################### endDash

def get_pub_data(request, org_level, area_id):
    print(org_level)
    print(area_id)
    main_dash_data = get_public_dash_ovc_hiv_status(org_level, area_id)
    return JsonResponse(main_dash_data, content_type='application/json',
                        safe=False)


def get_ovc_active_hiv_status(request, org_level, area_id):
    print(org_level)
    print(area_id)
    main_dash_data = _get_ovc_active_hiv_status(org_level, area_id)
    return JsonResponse(main_dash_data, content_type='application/json',
                        safe=False)


def get_ovc_served_stats(request, org_level, area_id, funding_partner, funding_part_id, period_type):
    main_dash_data = _get_ovc_served_stats(org_level, area_id, funding_partner, funding_part_id, period_type)
    return JsonResponse(main_dash_data, content_type='application/json',
                        safe=False)


def fetch_cbo_list(request):
    return JsonResponse(get_cbo_list(), content_type='application/json',
                        safe=False)


def get_locality_data(request):
    print("locality data")
    locality_data = fetch_locality_data()
    return JsonResponse(locality_data, content_type='application/json',
                        safe=False)


# ################### dash
def get_total_ovc_ever(request, org_level, area_id):
    print("total ovc ever")
    total_ovc_ever = fetch_total_ovc_ever(request, None, org_level, area_id)
    return JsonResponse(total_ovc_ever, content_type='application/json', safe=False)


def get_total_ovc_ever_exited(request, org_level, area_id):
    print("total ovc ever exited")
    total_ovc_ever_exited = fetch_total_ovc_ever_exited(request, None, org_level, area_id)
    return JsonResponse(total_ovc_ever_exited, content_type='application/json', safe=False)


def get_total_wout_bcert_at_enrol(request, org_level, area_id):
    print("without birthcert at enrolment")
    total_wout_bcert_at_enrol = fetch_total_wout_bcert_at_enrol(request, None, org_level, area_id)
    return JsonResponse(total_wout_bcert_at_enrol, content_type='application/json', safe=False)


def get_total_w_bcert_2date(request, org_level, area_id):
    print("all with birthcert to date")
    total_w_bcert_2date = fetch_total_w_bcert_2date(request, None, org_level, area_id)
    return JsonResponse(total_w_bcert_2date, content_type='application/json', safe=False)


def get_total_s_bcert_aft_enrol(request, org_level, area_id):
    print("all served birthcert after enrolment")
    total_s_bcert_aft_enrol = fetch_total_s_bcert_aft_enrol(request, None, org_level, area_id)
    return JsonResponse(total_s_bcert_aft_enrol, content_type='application/json', safe=False)

    # --------graphs-byperiod-------#


def get_new_ovcregs_by_period(request, org_level, area_id, funding_partner, funding_part_id, period_type):
    # print "new ovcregs by period with month_year="+month_year
    new_ovcregs_by_period = fetch_new_ovcregs_by_period(request, org_level, area_id, funding_partner, funding_part_id,
                                                        period_type)
    return JsonResponse(new_ovcregs_by_period, content_type='application/json', safe=False)


def get_active_ovcs_by_period(request, org_level, area_id, funding_partner, funding_part_id, period_type):
    pass
    # print "active ovcregs by period with month_year="+month_year
    # active_ovcs_by_period=fetch_active_ovcs_by_period(request, org_level,area_id,funding_partner,funding_part_id,period_type)
    # return JsonResponse(active_ovcs_by_period, content_type='application/json', safe=False)


def get_exited_ovcs_by_period(request, org_level, area_id, funding_partner, funding_part_id, period_type):
    # print "exited ovcregs by period with month_year="+month_year
    exited_ovcs_by_period = fetch_exited_ovcs_by_period(request, org_level, area_id, funding_partner, funding_part_id,
                                                        period_type)
    return JsonResponse(exited_ovcs_by_period, content_type='application/json', safe=False)


def get_exited_hsehlds_by_period(request, org_level, area_id, funding_partner, funding_part_id, period_type):
    # print "exited hsehlds by period with month_year="+month_year
    exited_hsehlds_by_period = fetch_exited_hsehlds_by_period(request, org_level, area_id, funding_partner,
                                                              funding_part_id, period_type)
    return JsonResponse(exited_hsehlds_by_period, content_type='application/json', safe=False)


def get_served_bcert_by_period(request, org_level, area_id, month_year):
    # print "served bcert by period with month_year="+month_year
    served_bcert_by_period = fetch_served_bcert_by_period(request, None, org_level, area_id, month_year)
    return JsonResponse(served_bcert_by_period, content_type='application/json', safe=False)


def get_u5_served_bcert_by_period(request, org_level, area_id, month_year):
    # print "u5 served bcert by period with month_year="+month_year
    u5_served_bcert_by_period = fetch_u5_served_bcert_by_period(request, None, org_level, area_id, month_year)
    return JsonResponse(u5_served_bcert_by_period, content_type='application/json', safe=False)
    # --------graphs-byperiod-------#


# ################### endDash

def get_hiv_suppression_data(request, org_level, area_id):
    hiv_suppression_data = get_ovc_hiv_status(request, None, org_level, area_id)
    return JsonResponse(hiv_suppression_data, content_type='application/json',
                        safe=False)


def get_ever_tested_hiv(request, org_level, area_id):
    ever_tested = get_ever_tested_for_HIV(request, None, org_level, area_id)
    return JsonResponse(ever_tested, content_type='application/json',
                        safe=False)


@login_required(login_url='/login/')
def home(request):
    """Some default page for the home page / Dashboard."""
    try:
        vals = get_dashboard(request)
        return render(request, 'dashboard.html', vals)
    except Exception as e:
        print(('dashboard error - %s' % (str(e))))
        raise e


def get_dashboard(request):
    """Some default page for the home page / Dashboard."""
    my_dates, my_cvals = [], []
    my_ovals, my_kvals = [], []
    my_dvals = []
    try:
        user_key = 'dash_%s' % (request.user.id)
        value = mc.get(user_key)
        if value:
            print(('In memcache Dashboard - %s' % (user_key)))
            return value
        else:
            print(('Set new Dashboard - %s' % (user_key)))
        dash = dashboard(request)
        start_date = datetime.now() - timedelta(days=21)
        summary = {}
        summary['org_units'] = '{:,}'.format(dash['org_units'])
        summary['children'] = '{:,}'.format(dash['children'])
        summary['guardians'] = '{:,}'.format(dash['guardian'])
        summary['workforce'] = '{:,}'.format(dash['workforce_members'])
        summary['cases'] = '{:,}'.format(dash['case_records'])
        summary['pending'] = '{:08}'.format(dash['pending_cases'])
        # summary['hiv_status'] = dash['hiv_status']

        # OVC care
        odash = ovc_dashboard(request)
        ovc = {}
        ovc['org_units'] = '{:,}'.format(odash['org_units'])
        ovc['children'] = '{:,}'.format(odash['children'])
        ovc['children_all'] = '{:,}'.format(odash['children_all'])
        ovc['guardians'] = '{:,}'.format(odash['guardian'])
        ovc['guardians_all'] = '{:,}'.format(odash['guardian_all'])
        ovc['workforce'] = '{:,}'.format(odash['workforce_members'])
        ovc['cases'] = '{:,}'.format(odash['case_records'])
        ovc['pending'] = '{:08}'.format(odash['pending_cases'])
        ovc['household'] = '{:,}'.format(odash['household'])
        ovc['hiv_status'] = odash['hiv_status']
        ovc['domain_hiv_status'] = odash['domain_hiv_status']
        child_regs = odash['child_regs']
        ovc_regs = odash['ovc_regs']
        case_regs = odash['case_regs']
        case_cats = dash['case_cats']
        for date in range(0, 22, 2):
            end_date = start_date + timedelta(days=date)
            show_date = datetime.strftime(end_date, "%d-%b-%y")
            final_date = str(show_date).replace(' ', '&nbsp;')
            my_dates.append("[%s, '%s']" % (date, final_date))
        for vl in range(1, 22):
            t_date = start_date + timedelta(days=vl)
            s_date = datetime.strftime(t_date, "%d-%b-%y")
            k_count = child_regs[s_date] if s_date in child_regs else 0
            o_count = ovc_regs[s_date] if s_date in ovc_regs else 0
            c_count = case_regs[s_date] if s_date in case_regs else 0
            my_cvals.append("[%s, %s]" % (vl, c_count))
            my_kvals.append("[%s, %s]" % (vl, k_count))
            my_ovals.append("[%s, %s]" % (vl, o_count))
        dates = ', '.join(my_dates)
        kvals = ', '.join(my_kvals)
        cvals = ', '.join(my_cvals)
        ovals = ', '.join(my_ovals)
        my_dvals, cnt = [], 0
        colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
                  '#ffff33']
        reg_ovc = request.session.get('reg_ovc', 0)
        ovc_criterias = False
        total_ovc = odash['children_all']
        if reg_ovc and total_ovc > 0:
            # Eligibility criteria
            ovc_criterias = True
            other_case = 0
            cat_name = "Missing Criteria"
            cat_data = total_ovc
            cnt = 0
            my_data = '{label: "%s", data: %s, color: "%s"}' % (
                cat_name, cat_data, colors[cnt])
            my_dvals.append(my_data)
        else:
            # Case category names
            cnames = get_dict(field_name=['case_category_id'])
            other_case = 0
            for case_cat in case_cats:
                cat_id = case_cat['case_category']
                cat_data = case_cat['unit_count']
                if cnt > 4:
                    other_case += cat_data
                else:
                    cnm = cnames[cat_id] if cat_id in cnames else cat_id
                    cat_name = cnm[:16] + ' ...' if len(cnm) > 16 else cnm
                    my_data = '{label: "%s", data: %s, color: "%s"}' % (
                        cat_name, cat_data, colors[cnt])
                    my_dvals.append(my_data)
                cnt += 1
        if not case_cats and not ovc_criterias:
            my_dvals.append('{label: "No data", data: 0, color: "#fd8d3c"}')
        if other_case > 0:
            my_dvals.append(
                '{label: "Others", data: %s, color: "#fb9a99"}' % (other_case))
        dvals = ', '.join(my_dvals)
        ovc_params = odash['ovc_summary']
        om_data = '[0, {m0}], [1, {m1}], [2, {m2}], [3, {m3}], [4, {m4}]'
        of_data = '[0, {f0}], [1, {f1}], [2, {f2}], [3, {f3}], [4, {f4}]'
        omdata = om_data.format(**ovc_params)
        ofdata = of_data.format(**ovc_params)
        vals = {'status': 200, 'dates': dates, 'kvals': kvals,
                'dvals': dvals, 'cvals': cvals, 'data': summary,
                'ovals': ovals, 'ovc': ovc, 'omvals': omdata,
                'ofvals': ofdata}
        mc.set(user_key, vals, 6 * 60 * 60)
    except Exception as e:
        print(('dashboard error - %s' % (str(e))))
        raise e
    else:
        return vals


def access(request):
    """Some default page for access login."""
    try:
        if request.method == 'POST':
            response = access_request(request)
            return JsonResponse(response, content_type='application/json',
                                safe=False)
        return render(request, 'home.html', {'status': 200, })
    except Exception as e:
        raise e


def handler_400(request, exception, template_name="400.html"):
    """Some default page for Bad request error page."""
    # response = '/not-found'
    # response.status_code = 400
    # return render(request, response, template_name)
    try:
        return render(request, '400.html', {'status': 400})
    except Exception as e:
        raise e


def handler_404(request, exception):
    """Some default page for the Page not Found."""
    try:
        todate = datetime.now()
        ts = todate.strftime("%d %b %Y %H:%M:%S")
        context = {'status': 404}
        etype, value, traceback = sys.exc_info()
        context['traceback'] = traceback
        context['value'] = value
        context['etype'] = etype
        context['ts'] = ts
        return render(request, '404.html', context)
    except Exception as e:
        raise e


def handler_500(request):
    """Some default page for Server Errors."""
    try:
        todate = datetime.now()
        ts = todate.strftime("%d %b %Y %H:%M:%S")
        context = {'status': 500}
        etype, value, traceback = sys.exc_info()
        context['traceback'] = traceback
        context['value'] = value
        context['etype'] = etype
        context['ts'] = ts
        return render(request, '500.html', context)
    except Exception as e:
        raise e


def csrf_failure(request, reason):
    """Some default page for CSRF error."""
    try:
        return render(request, 'csrf.html', {'status': 500, 'reason': reason})
    except Exception as e:
        raise e



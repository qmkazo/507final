import secrets
import plotly
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import operator
import instances

def compare_tuition(state_url,state):
    list1=instances.get_sites_for_state(state_url)
    namelist=[]
    tuition_in_list=[]
    tuition_out_list=[]

    for item in list1:
        if item.tuition_in != 0 and item.tuition_out != 0:
            namelist.append(item.name)
            tuition_in_list.append(int(item.tuition_in))
            tuition_out_list.append(int(item.tuition_out))
        else:
            pass

    chart_studio.tools.set_credentials_file(username=secrets.plotly_username, api_key=secrets.plotly_key)

    trace_1 = go.Bar(
        x=namelist,
        y=tuition_in_list,
        name="Tuition (in state)",
        marker=dict(
                
                line=dict(
                    color='rgb(8,48,107)',
                    width=0),
            ),
            opacity=0.6
    )
    
    trace_2 = go.Bar(
        x=namelist,
        y=tuition_out_list,
        name="Tuition (out of state)",
        marker=dict(
                
                line=dict(
                    color='rgb(8,48,107)',
                    width=0),
            ),
            opacity=0.6
    )
    
    trace=[trace_1,trace_2]
    trace_layout=go.Layout(title=f'Tuition of top colleges in {state}', yaxis_title='Tuition/$', yaxis_tickformat = '$,.0')

    fig = go.Figure(data=trace,layout=trace_layout)

    fig.show()


def compare_enrollment(state_url,state):
    list1=instances.get_sites_for_state(state_url)
    namelist=[]
    enrollment_list=[]
    
    for item in list1:
        if item.enrollment !='' and item.enrollment != 0 :
            namelist.append(item.name)
            enrollment_list.append(int(item.enrollment))
            
        else:
            pass

    chart_studio.tools.set_credentials_file(username=secrets.plotly_username, api_key=secrets.plotly_key)

    trace = go.Bar(
        x=namelist,
        y=enrollment_list,
        name="Enrollment",
        
        marker=dict(
                color=['#FF0000','#FF6100','#FFD700','#3D9140','#87CEEB','#4169E1','#DA70D6','#FFFFCD','#FFFFFF','#000000'],
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            opacity=0.6
        
        
        
        # marker=dict(
                
        #         line=dict(
        #             color='rgb(8,48,107)',
        #             width=0),
        #     ),
        #     opacity=0.6
    )
    

    trace_layout=go.Layout(title=f'Enrollment of top colleges in {state}', yaxis_title='Enrollment', yaxis_tickformat = ',.0')

    fig = go.Figure(data=trace,layout=trace_layout)

    fig.show()






def show_college_info(state_url,state):
    list2=instances.get_sites_for_state(state_url)
    ranklist=[]
    namelist=[]
    addresslist=[]
    phonelist=[]
    tuition_in_list=[]
    tuition_out_list=[]
    enrollmentlist=[]

    for item in list2:
        try:
            ranklist.append(item.rank)
        except:
            ranklist.append('No rank info')
       
        try:    
            namelist.append(item.name)
        except:
            namelist.append('No name info')
        
        try:    
            addresslist.append(item.city)
        except:
            addresslist.append('No address info')
        
        try:    
            phonelist.append(item.phone)
        except:
            phonelist.append('No phone info')
    
        if item.tuition_in != 0:    
            tuition_in_list.append('$'+str(item.tuition_in))
        else:
            tuition_in_list.append('No tuition info')
        
        if item.tuition_out != 0:   
            tuition_out_list.append('$'+str(item.tuition_out))
        else:
            tuition_out_list.append('No tuition info')
        
        if item.enrollment != '':
            enrollmentlist.append(item.enrollment)
        else:
            enrollmentlist.append('No enrollment info')



    
    trace = go.Table(
        header=dict(values=['Rank','Name','Address','Phone','Tuition (in state)','Tuition (out of state)','Enrollment']),
        cells=dict(values=[ranklist,namelist,addresslist,phonelist,tuition_in_list,tuition_out_list,enrollmentlist])
    #     marker=dict(
    #             color=['#FF0000','#FF6100','#FFD700','#3D9140','#87CEEB','#4169E1','#DA70D6','#FFFFCD','#FFFFFF','#000000'],
    #             line=dict(
    #                 color='rgb(8,48,107)',
    #                 width=1.5),
    #         ),
    #         opacity=0.6
    )
    
    trace_layout = go.Layout(title=f'Top colleges in {state}')

    fig_2 = go.Figure(data=trace,layout=trace_layout)
    
    fig_2.show()
    

def show_map_info(college_object):
    location_dict=instances.get_nearby_places(college_object)
    
    namelist=[]
    categorylist=[]
    streetlist=[]
    citylist=[]

    for places in location_dict['searchResults']:
        
        namelist.append(places["name"])
        
        if places['fields']["group_sic_code_name"] != '':
            categorylist.append(places['fields']["group_sic_code_name"])
        else:
            categorylist.append("No category info")
        
        if places['fields']["address"] != '':
            streetlist.append(places['fields']["address"])
        else:
            streetlist.append("No address info")
        
        if places['fields']["city"] != '':
            citylist.append(places['fields']["city"])
        else:
            citylist.append("No area info")

    trace = go.Table(
        header=dict(values=['name','category','Address','Area']),
        cells=dict(values=[namelist,categorylist,streetlist,citylist])
    )
    
    trace_layout=go.Layout(title=f'Places near {college_object.name}')

    fig_2 = go.Figure(data=trace,layout=trace_layout)
    
    fig_2.show()
    
# show_map_info(instances.get_college_instance('https://www.usnews.com/best-colleges/nyu-2785'))
# show_map_info(instances.get_college_instance('https://www.usnews.com/best-colleges/university-of-michigan-ann-arbor-9092'))

#Importing necessary libraries
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_auth
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime 

dash_app = dash.Dash(__name__)  #creating a dash object

app = dash_app.server  


dash_app.config.suppress_callback_exceptions = True  #For not triggering the exceptions

dash_app.layout = html.Div(children = [
    html.Div(" "),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#Main Page / Home page of the websote
index_page =   html.Div(children = [
                  html.Div(className="header", children = [
    	    	html.Div(className="logo", children = [
		   html.Img(src= '/assets/ERM_Logo.png')
		]),
		html.Div(className="banner",children = [
		   html.H1("Dynamic Crash Prevention Solution")
		]),
 		html.Div(className="header-images",children = [
		   html.Div(className="header-image1",children = [
 			html.Img(src= '/assets/DCP_Img_1.jpg',width=250,height=75)
		   ]),
		   html.Div(className="header-image2",children = [
 			html.Img(src= '/assets/DCP_Img_2.jpg',width=250,height=75)
		   ]),
		   html.Div(className="header-image3",children = [
 			html.Img(src= '/assets/DCP_Img_3.jpg',width=250,height=75)
		   ])
		])
           
             
]),
html.Div(className = "bg",children = [
 html.Div(className = "mp-route-option", children = [
                html.Div(className="mp-upper-part",children = [
                     html.Div(className="mp-route1-img",children = [
			  html.Div("Jamnagar to Rajkot",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Jam_Rajkot.png",width=800,height=300),href = "/JRK")
                     ]),
                     html.Div(className="mp-route2-img",children = [
       	    		  html.Div("Jamnagar to Naghedi",style={'background-color':'Dark Green','color':'White'}),
                          html.A(html.Img(src = "/assets/Jamnagar_Naghedi.png",width=800,height=300),href = "/JNG")
                     ]),
                     html.Div(className="mp-route3-img",children = [
			  html.Div("Vadodra IOCL to Vemali Vadodra",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Vadodra_Internal.png",width=800,height=300),href = "/Sample")
                     ]),
                     html.Div(className="mp-route4-img",children = [
			  html.Div("Vadodra to Rajkot",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Vadodra_Rajkot.png",width=800,height=300),href = "/")
                     ])
                ])
          ])
])
])


@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/JNG':  #if url is observations then render the layout of Safety Observations
        return real_time_layout
    else:
        return index_page 

real_time_layout =  html.Div(children = [ 
                      #html.Button("Show Graph",id = "Show Graph"),
					  dcc.Interval(
						id='interval-component',
						interval=2*1000, # in milliseconds
						n_intervals=0
						),
                      dcc.Graph(id="Scatterplotmap",figure={'layout': { 'clickmode': 'event+select'}},style={'width':'1900px','height':'900px'}),
					  html.Div(id = "Driver_UI",style={'background-color':'white'}),
					  html.Div(id = "Alert Message",style={'background-color':'white'}),
					  html.Div(id="show_message"),
					  
					])



#Reading csv file
route_data= pd.read_csv("Trip_Data_v1.csv")

@dash_app.callback(
  	dash.dependencies.Output('Scatterplotmap', 'figure'),
    	[dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(n):
	if n>-1:
		key_api = "pk.eyJ1IjoiYWRpdHlhdGFvcmkiLCJhIjoiY2s1NTMzM205MGJyNjNla2JxZDRxdHBvdiJ9.OmOHzC_AyvWfjv9Sulz3tw"
		mapbox_access_token = key_api
		#For moving the vehicle
		current_pos = route_data[route_data["Time Interval"]==n+1]
		
		#to find unique number of drivers
		unique_drivers = current_pos["Driver ID"].unique()
		num_drivers = len(unique_drivers)
		mutiple_markers = ["bus"]*num_drivers
		text_str = []
		driver_custom_data = []
		for dc in range(0,num_drivers):
			ind_driver_id= unique_drivers[dc]
			ind_customer_data = str(n) +"_"+ str(ind_driver_id)
			driver_custom_data.append(ind_customer_data)
		for nd in range(0,num_drivers):
			ind_driver = current_pos["Driver Name"].iloc[nd]
			ind_vehicle = current_pos["Vehicle Number"].iloc[nd]
			ind_risk_rating = current_pos["Risk Rating"].iloc[nd]
			ind_driving_hrs = current_pos["Continuous Driving Hours (HH_MM)"].iloc[nd]
			ind_overspeed = current_pos["Overspeeding"].iloc[nd]
			ind_lane_violations = current_pos["Lane Violations"].iloc[nd]
			ind_ha = current_pos["Harsh Accelaration"].iloc[nd]
			ind_hb = current_pos["Harsh Braking"].iloc[nd]
			ind_hc = current_pos["Harsh Cornering"].iloc[nd]
			ind_distr = current_pos["Distractions "].iloc[nd]
			ind_yawn = current_pos["Yawning"].iloc[nd]
			
			ind_str_text = "Driver Name: "+ind_driver+"<br>Vehicle Number:"+ind_vehicle+"<br>Risk Rating: "+str(ind_risk_rating)+"<br> Continuous Driving Hours"+str(ind_driving_hrs)+"<br>Overspeeding: "+str(ind_overspeed)+"<br>Lane Violations: "+str(ind_lane_violations)+"<br>Harsh Accelaration: "+str(ind_ha)+"<br>Harsh Braking: "+str(ind_hb)+"<br>Harsh Cornering: "+str(ind_hc)+"<br>Distractions: "+str(ind_distr)+"<br>Yawning: "+str(ind_yawn)
			
			text_str.append(ind_str_text)
				
		
		#print(current_pos)
		weight = current_pos.Weight
		#For plotting a route the vehicle follows 
		line_route = route_data[route_data["Time Interval"].isin(range(1,n))]
		#print(line_route)
		line_route_lat = line_route.Latitude#Latitudes of route followed till now 
		line_route_lon = line_route.Longitude #Longitudes of route followed till now
		line_route_wt = line_route.Weight  
		#Changing the colour on the basis of the risk index
		green_code = 'rgb(0,255,0)'  #For safe
		amber_code = 'rgb(255,191,0)'  #For monitor
		red_code = 'rgb(255,0,0)'  #For take action
		fig = go.Figure()  
		#desired_color = green_code if weight==1 else (amber_code if weight==2 else red_code)
		#print(desired_color)
		overspeeding = current_pos["Overspeeding"].iloc[0]
		driver_name = current_pos["Driver Name"].iloc[0]
		time_int = n
		#cust_list = []
        #cust_list.append(
        #Layer for moving the vehicle in the real time
		fig.add_trace(go.Scattermapbox(
				lat=current_pos.Latitude,
				lon=current_pos.Longitude,
				mode='markers',
				marker=go.scattermapbox.Marker(
					size=18,
					color= weight,
					opacity=0.7,
					cmin = 1,
					cmax = 3,
					cmid = 2,
					colorscale = [[0, 'rgb(0,255,0)'],[0.5,'rgb(255,165,0)'], [1, 'rgb(255,0,0)']]
				),
				text="",
				hoverinfo='text',
				
			))
		
		
		#Layer for showing the color of the icon
		fig.add_trace(go.Scattermapbox(
				lat=current_pos.Latitude,
				lon=current_pos.Longitude,
				mode='markers',
				marker = {'size': 14, 'symbol': mutiple_markers},
				text= text_str,
				customdata=driver_custom_data
				)
			)
		
		if False: 
			#Layer for showing the route the vehicle followed till now
			fig.add_trace(go.Scattermapbox(
				lat=line_route_lat,
				lon=line_route_lon,
				mode='lines',
				line = {'width':4,'color':'rgb(255,192,0)'}
				)
				)        
		
		
		

		
		fig.update_layout(
			title='Jamnagar Route',
			autosize=True,
			hovermode='closest',
			showlegend=False,
			mapbox=go.layout.Mapbox(
				accesstoken=mapbox_access_token,
				bearing=0,
				center=go.layout.mapbox.Center(
					lat=22.33036,
					lon=69.86321
				),
				pitch=0,
				zoom=12,
				style='streets'
			),
		)
		#print(fig)
		return fig

@dash_app.callback(
    dash.dependencies.Output('show_message', 'children'),
    [dash.dependencies.Input('Scatterplotmap', 'clickData')])

def click_processing(clickData):
	if clickData!=None:
		#print("Click Processing")
		#print(clickData)
		X = clickData
		Y = X["points"][0]
		ind_driver_meta = Y['customdata']
		split_op = ind_driver_meta.split("_")
		ind_interval = split_op[0]
		ind_driver_id = split_op[1]
		#print("Interval ID: "+str(ind_interval))
		#print("Driver ID: "+str(ind_driver_id))
		r_int_data = route_data[route_data["Time Interval"]==int(ind_interval)]
		r_index = list(r_int_data.index)
		driver_record =  r_int_data[r_int_data["Driver ID"]==int(ind_driver_id)].index 
		driver_index = r_index.index(driver_record)
		r_int_data["Longitude"] = round(r_int_data["Longitude"],5)
		r_int_data["Latitude"] = round(r_int_data["Latitude"],5)
		#print("r_int = "+str(driver_index))
		return dash_table.DataTable(
					id='Driver Details',
					data=r_int_data.to_dict('records'),
					columns=[
						{"name": i, "id": i,"selectable":True} for i in r_int_data.columns
						],
					row_selectable="single",
					style_data_conditional=[{
						"if": {"row_index":driver_index},
						"backgroundColor": "#3D9970",
						'color': 'white'
		}],
		style_table={'fontFamily': 'Times New Roman'
                    }, 
		style_cell = {'textAlign':'left', 'fontFamily': 'Times New Roman'},
		style_cell_conditional = [
					{'if': {'column_id':'Route'}, 'width':'25%'},
					{'if': {'column_id':'Driver Name'}, 'width':'25%'}
		])

@dash_app.callback( 
	dash.dependencies.Output('Driver_UI','children'),
	[dash.dependencies.Input('Driver Details','derived_virtual_selected_rows')])
	
def show_driver_ui(derived_virtual_selected_rows):
	if derived_virtual_selected_rows ==[]:
		print("Empty")
	else: 
		#print(derived_virtual_selected_rows)
		selected_driver = route_data.iloc[derived_virtual_selected_rows[0]]
		d_name = selected_driver["Driver Name"]
		veh_num = selected_driver["Vehicle Number"]
		
		return html.Div([
			html.B("Driver Name: "+d_name),
			html.Br(),
			html.Img(src = dash_app.get_asset_url("Driver_1.jpg")),
			html.Br(),
			html.B("Vehicle Number:" +veh_num),
			html.Br(),
			html.B("Time:"+str(datetime.now())),
			html.Br(),
			html.B("Temperature: 26 C"),
			html.Br(),
			html.Button("ALERT",id="Send Alert",style={'font-size': '20px'})
		])
    
@dash_app.callback( 
	dash.dependencies.Output('Alert Message','children'),
	[dash.dependencies.Input('Send Alert','n_clicks')])

def show_alert_message(n_clicks):
	if n_clicks>0:
		return html.Div([html.H1("Alert Sent Successfully")])
		
if __name__ == '__main__':
    dash_app.run_server()
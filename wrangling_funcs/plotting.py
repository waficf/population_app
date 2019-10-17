import plotly.graph_objs as go

from wrangling_funcs.cleaning_fn import *


def return_figures():

	params= {'format': 'json', 'per_page': '1000', 'date':'1960:2017'}
	data = full_query('SP.POP.TOTL', params)

	df = extract_data('/Users/wafic/Documents/population_app/Data')

	df_country = country_data(df)

	df_country_17 = df_country[df_country.year == '2017']

	graph_one = [dict(type = 'choropleth',
	                 locations = df_country_17['3let'],
	                 z= df_country_17['value'],
	                 text = df_country_17['country'],
	                 colorscale = 'Viridis',
	                 autocolorscale = False,
	                 reversescale = True,
	                 marker = dict(
	                     line = dict(
	                         color = 'rgb(180, 180, 180)',
	                         width = 0.5)),
	                  colorbar = dict(title = 'Population (Billions)'),
	                 )]

	layout_one = dict(margin = dict(
	    l = 30,
	    r = 10,
	    b = 0,
	    t = 10,
	    pad = 4
	),
	    geo =dict(
	    landcolor = 'lightgray',
	    showland = True,
	    showcountries = True,
	    countrycolor = 'gray',
	    countrywidth = 0.5,
	    showframe = False,
	    showcoastlines = False,
	    projection = dict(
	        type='mercator'
	    )
	    )
	                 )


	df_country_60 = df_country[df_country.year == '1960']

	graph_two = [dict(type = 'choropleth',
	                 locations = df_country_60['3let'],
	                 z= df_country_60['value'],
	                 text = df_country_60['country'],
	                 colorscale = 'Viridis',
	                 autocolorscale = False,
	                 reversescale = True,
	                 marker = dict(
	                     line = dict(
	                         color = 'rgb(180, 180, 180)',
	                         width = 0.5)),
	                  colorbar = dict(title = 'Population (Millions)'),
	                 )]

	layout_two = dict(margin = dict(
	    l = 30,
	    r = 10,
	    b = 0,
	    t = 10,
	    pad = 4
	),
	    geo =dict(
	    landcolor = 'lightgray',
	    showland = True,
	    showcountries = True,
	    countrycolor = 'gray',
	    countrywidth = 0.5,
	    showframe = False,
	    showcoastlines = False,
	    projection = dict(
	        type='mercator'
	    )
	    )
	                 )




	decades = ['1960', '1970', '1980', '1990', '2000', '2010', '2017']

	df_classif = income_classification(df)

	df_classif_dec = df_classif[(df_classif.year.isin(decades))&(df_classif.country.isin(['High income', 'Low income']))]

	df_classif_dec = df_classif_dec.drop(columns='code')

	high_low = df_classif_dec.country.unique().tolist()

	graph_three = []

	for country in high_low:
		x_val = df_classif_dec[df_classif_dec['country'] == country].year.tolist()
		y_val = df_classif_dec[df_classif_dec['country'] == country].value.tolist()
		graph_three.append(
        	go.Scatter(x=x_val, 
        		y=y_val, 
        		mode='lines+markers', 
        		marker = dict(
        			size=2.25,
        			),
        		name=country)
        	)
		layout_three = dict(
        	# title = 'Difference in Population Growth between Highest and Lowest',
        	xaxis = dict(
        		title = 'Year',
        		dtick = 5
        		),
        	yaxis = dict(
        		title = 'Population'
        		),
        	hovermode = 'closest',
        	)

	graph_four = []

	for country in high_low:
		x_val = df_classif_dec[df_classif_dec['country'] == country].year.tolist()
		y_val = df_classif_dec[df_classif_dec['country'] == country].value.tolist()
		graph_four.append(
        	go.Scatter(x=x_val, 
        		y=y_val, 
        		mode='lines+markers', 
        		marker = dict(
        			size=2.25,
        			),
        		name=country)
        	)
		layout_four = dict(
        	# title = 'Difference in Population Growth between Highest and Lowest',
        	xaxis = dict(
        		title = 'Year',
        		dtick = 5
        		),
        	yaxis = dict(
        		title = 'Population'
        		),
        	hovermode = 'closest',
        	)


	figures = []
	graphs = (graph_one, graph_two, graph_three, graph_four)
	layouts = (layout_one, layout_two, layout_three, layout_four)
	config = dict(responsive = True)

	for graph, layout in zip(graphs, layouts):
		figures.append(dict(data=graph, layout=layout, config=config))

	return figures

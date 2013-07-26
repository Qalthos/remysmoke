<%inherit file="local:templates.master"/>

<%def name='head()'>
	<link href="/css/graph.css" media="screen" type="text/css" rel="stylesheet">
</%def>

%for name, chart in charts.items():
	Punchcard for ${name}
	${chart | n}
%endfor

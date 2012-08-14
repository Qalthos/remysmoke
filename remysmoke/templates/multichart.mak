<%inherit file="local:templates.master"/>

%for name, chart in charts.items():
	Punchcard for ${name}
	${chart | n}
%endfor

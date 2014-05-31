<%inherit file="local:templates.master"/>

<%def name='head()'>
	<link href="/css/graph.css" media="screen" type="text/css" rel="stylesheet">
</%def>

<div style='float:left; width:30%;'>
  <p>Cigarettes smoked over time</p>
  <form>
  <input name='weeks' type='range' min=1 max=52 value=${weeks if weeks else 1} />
    <input type='submit' />
  </form>
  <p>Other</p>
  <li>
    <ul><a href="${tg.url('/graph?graph=punch')}" class="${('', 'active')}">Smoking Punchcard</a></li>
  </li>
</div>

<div style='float:left; width:70%'>
  ${widget | n}
</div>

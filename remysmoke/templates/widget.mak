<%inherit file="local:templates.master"/>

<%def name='head()'>
	<link href="/css/graph.css" media="screen" type="text/css" rel="stylesheet">
</%def>

<form action=${tg.url('graph')} class='chart'>
  <fieldset>
    <h2><span>Histogram</span></h2>
    <input name='weeks' type='range' min=1 max=52 value=${weeks if weeks else 1} />
      <input type='submit' class='submit' />
  </fieldset>
  <fieldset>
    <h2><span>Punchcard</span></h2>
    <a href="${tg.url('/graph?graph=punch')}" class="${('', 'active')}">Smoking Punchcard</a></li>
  </fieldset>
  <%include file='local:templates.user_picker'/>
</form>

<div style='height:230px'>
  ${widget | n}
</div>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/mobile_style.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
</head>
<body class="${self.body_class()}">
  ${self.header()}
  ${self.content_wrapper()}
</body>

<%def name="content_wrapper()">
    <div id="content">
      ${self.body()}
    </div>
</%def>

<%def name="body_class()"> </%def>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()"> </%def>

<%def name="header()">
  <div id="header">
    <img src="${tg.url('/images/smoke_face.png')}" />
  	<h1>Remysmoke</h1>
  </div>
</%def>

</html>

<%@ page contentType="text/html; charset=UTF-8" language="java" %>

<html>
<head>
<title>calculator</title>
</head>

<body>
<form action="calcResult.jsp" method="post" >
<h1>Number 1: ${param.num1}</h1>
<h1>Number 2: ${param.num2}</h1>
<h1>Sum: ${param.num2+param.num1}</h1>


</form>

</body>

</html>
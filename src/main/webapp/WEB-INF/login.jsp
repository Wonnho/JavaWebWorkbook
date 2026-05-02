<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<html>
<head>
    <title>todo login</title>
</head>
<body>

<c:if test="${param.result=='error'}">
<h1>Login Error</h1>
</c:if>

<form action="/login" method="post">
<input type="text" name="todoid">
<input type="text" name="todopw">
<button type="submit">Login</button>
</form>
</body>
</html>
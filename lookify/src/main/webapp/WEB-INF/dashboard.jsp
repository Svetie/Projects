<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ page isErrorPage="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form"%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="ISO-8859-1">
	<title>Dashboard</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
	<a href="/songs/new">Add New</a>
	<a href="/topten">Top Songs</a>

	<form:form action="/search" method="post" modelAttribute="song">
	<div class="form-group">
		<form:label path="artist"></form:label>
		<form:errors path="artist" class="text-danger"/>
		<form:input path="artist" name="artistToFind"/>
	</div>
	<input type="submit" value="Search Artists" class="btn btn-primary"/>
	</form:form>

	<table class="table">
		<thead>
			<tr>
				<th scope="col">Title</th>
				<th scope="col">Rating</th>
				<th scope="col">Actions</th>
			</tr>
		</thead>
		<tbody>
			<c:forEach var="song" items="${allSongs}">
				<tr>
					<th><a href="/songs/${song.id}">${song.title}</a></th>
					<td>${song.rating}</td>
					<td><a href="/delete/${song.id}">delete</a></td>
				</tr>
			</c:forEach>
		</tbody>
	</table>
</body>
</html>
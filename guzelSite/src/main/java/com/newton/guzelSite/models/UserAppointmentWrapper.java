package com.newton.guzelSite.models;

import java.util.Date;

import javax.validation.constraints.Email;
import javax.validation.constraints.Future;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Past;
import javax.validation.constraints.Size;

import org.springframework.format.annotation.DateTimeFormat;

public class UserAppointmentWrapper {
	
	@NotEmpty(message="Username is required!")
	@Size(min=3, max=30, message="Username must be between 3 and 30 characters")
	private String name;
	
    @NotNull(message="Choose a birthday date")
    @DateTimeFormat(pattern="yyyy-MM-dd")
    @Past(message="Date cannot be in the future")
    private Date birthday;
	
	@NotEmpty(message="Email is required!")
	@Email(message="Please enter a valid email!")	
	private String email;
	
	@NotNull(message="Choose a date")
    @DateTimeFormat(pattern="yyyy-MM-dd")
    @Future(message="Date cannot be in the past")
    private Date date;
    
    @NotNull(message="Choose time")
    private Date time;
    
    public UserAppointmentWrapper () {}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Date getBirthday() {
		return birthday;
	}

	public void setBirthday(Date birthday) {
		this.birthday = birthday;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public Date getDate() {
		return date;
	}

	public void setDate(Date date) {
		this.date = date;
	}

	public Date getTime() {
		return time;
	}

	public void setTime(Date time) {
		this.time = time;
	}
}

package com.newton.guzelSite.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.newton.guzelSite.models.User;
import com.newton.guzelSite.repositories.UserRepository;

@Service
public class UserService {
	
	@Autowired
	private UserRepository userRepo;
	
	public UserService(UserRepository userRepo) {
		this.userRepo = userRepo;
	}
	
	public User saveUser(User user) {
		return this.userRepo.save(user);
	}
}

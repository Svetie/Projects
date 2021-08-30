package com.newton.guzelSite.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.newton.guzelSite.models.BeautyService;
import com.newton.guzelSite.repositories.ServiceRepository;

@Service
public class ServiceService {

	@Autowired
	private ServiceRepository serviceRepo;

	public BeautyService createService(BeautyService service) {
		return this.serviceRepo.save(service);
	}
	
	public List<BeautyService> getAllServices(){
		return this.serviceRepo.findAll();
	}
}

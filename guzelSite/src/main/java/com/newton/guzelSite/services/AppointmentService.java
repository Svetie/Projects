package com.newton.guzelSite.services;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.newton.guzelSite.models.Appointment;
import com.newton.guzelSite.repositories.AppointmentRepository;

@Service
public class AppointmentService {
	
	@Autowired
	private AppointmentRepository appointmentRepo;
	
	public AppointmentService(AppointmentRepository appointmentRepo) {
		this.appointmentRepo = appointmentRepo;
	}
	
	public Appointment saveAppointment(Appointment appointment) {
		return this.appointmentRepo.save(appointment);
	}
}

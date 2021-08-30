package com.newton.guzelSite.controllers;

import java.util.List;

import javax.servlet.http.HttpSession;
import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.newton.guzelSite.models.Appointment;
import com.newton.guzelSite.models.BeautyService;
import com.newton.guzelSite.models.User;
import com.newton.guzelSite.models.UserAppointmentWrapper;
import com.newton.guzelSite.services.AppointmentService;
import com.newton.guzelSite.services.ServiceService;
import com.newton.guzelSite.services.UserService;

@Controller
public class HomeController {
	
	@Autowired
	private ServiceService serviceService;
	
	@Autowired 
	private AppointmentService appointmentService;
	
	@Autowired
	private UserService userService;
	
	
	@GetMapping("/")
	public String home() {
		return "index.jsp";
	}
	
	
	// *******************************************
	//			Register
	// *******************************************
	
	// *******************************************
	//			Login
	// *******************************************
	
	// *******************************************
	//		Create Service: Admin Access ONLY!!
	// *******************************************
	@GetMapping("/create")
	public String servicePage(@ModelAttribute("service")BeautyService service) {
		// admin only
		return "tryToCreate.jsp";
	}
	
	@GetMapping("/create/service")
	public String createServicePage(@ModelAttribute("service")BeautyService service) {
		// admin only
		return "createService.jsp";
	}
	
	@PostMapping("/create/new/service")
	public String createNewService(@Valid @ModelAttribute("service")BeautyService service, 
			BindingResult result ) {
		if(result.hasErrors()) {
			return "createService.jsp";
		} else {
			this.serviceService.createService(service);
			return "redirect:/services";
		}
	}
	
	@GetMapping("/services")
	public String showServicesAndPrices(Model model, HttpSession session) {
		List<BeautyService> allServices = this.serviceService.getAllServices();
		model.addAttribute("allServices", allServices);
		return "services.jsp";
	}
	
	@GetMapping("/services/rus")
	public String showServicesAndPricesRus(Model model, HttpSession session) {
		List<BeautyService> allServices = this.serviceService.getAllServices();
		model.addAttribute("allServices", allServices);
		return "servicesRus.jsp";
	}
	
	@GetMapping("/appointment")
	public String appointment(@ModelAttribute("wrapper")UserAppointmentWrapper wrapper) {
		return "appointment.jsp";
	}
	
	@PostMapping("/make/appointment")
	public String makeAppointment(@Valid @ModelAttribute("wrapper")UserAppointmentWrapper wrapper,
			BindingResult result, RedirectAttributes redirectAttributes) {
		if(result.hasErrors()) {
			redirectAttributes.addFlashAttribute("error", "Error making an appointment");
			return "appointment.jsp";
		} else {
			System.out.println(wrapper.getName());
			User user = new User();
			Appointment appointment = new Appointment();
			
			appointment.setDate(wrapper.getDate());
			appointment.setTime(wrapper.getTime());
			
			user.setName(wrapper.getName());
			user.setBirthday(wrapper.getBirthday());
			user.setEmail(wrapper.getEmail());	
			
			appointment.setUser(user);
			List<Appointment> appointments = user.getAppointments();
			appointments.add(appointment);
			
			this.userService.saveUser(user);
			this.appointmentService.saveAppointment(appointment);
			
			
			redirectAttributes.addFlashAttribute("success", "You will get a confiramtion email within 24 hours");
			return "redirect:/";
			
		}
	}
	
	@GetMapping("/works")
	public String workPage() {
		return "works.jsp";
	}
}

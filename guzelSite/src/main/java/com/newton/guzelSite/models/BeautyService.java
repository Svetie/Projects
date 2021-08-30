package com.newton.guzelSite.models;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;
import javax.persistence.Table;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import org.springframework.format.annotation.DateTimeFormat;

@Entity
@Table(name="services")
public class BeautyService {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@NotEmpty(message="Username is required!")
	private String nameEng;
	
	@NotEmpty(message="Название необходимо!")
	private String nameRus;
	
	@NotEmpty(message="Description is required!")
	private String descriptionEng;
	
	@NotEmpty(message="Описание необходимо")
	private String descriptionRus;
	
	@NotNull
	private Integer price;
	
	 @Column(updatable=false)
	@DateTimeFormat(pattern="yyyy-MM-dd")
	private Date createdAt;
	@DateTimeFormat(pattern="yyyy-MM-dd")
	private Date updatedAt;
	
	@PrePersist
	protected void onCreate(){
	    this.createdAt = new Date();
	}
	@PreUpdate
	protected void onUpdate(){
	    this.updatedAt = new Date();
	}
		
	// --------------- Relationships ----------
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="appointment_id")
    private Appointment appointment;
    
    
    // ------------- Constructors --------------
    
    public BeautyService() {}
    
    public BeautyService(String nameEng, String nameRus, String descriptionEng, String descriptionRus, 
    		Integer price) {
    	this.nameEng = nameEng;
    	this.nameRus = nameRus;
    	this.descriptionEng = descriptionEng;
    	this.descriptionRus = descriptionRus;
    	this.price = price;
    }
	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public String getNameEng() {
		return nameEng;
	}
	public void setNameEng(String nameEng) {
		this.nameEng = nameEng;
	}
	public String getNameRus() {
		return nameRus;
	}
	public void setNameRus(String nameRus) {
		this.nameRus = nameRus;
	}
	public String getDescriptionEng() {
		return descriptionEng;
	}
	public void setDescriptionEng(String descriptionEng) {
		this.descriptionEng = descriptionEng;
	}
	public String getDescriptionRus() {
		return descriptionRus;
	}
	public void setDescriptionRus(String descriptionRus) {
		this.descriptionRus = descriptionRus;
	}
	public Integer getPrice() {
		return price;
	}
	public void setPrice(Integer price) {
		this.price = price;
	}
	public Date getCreatedAt() {
		return createdAt;
	}
	public void setCreatedAt(Date createdAt) {
		this.createdAt = createdAt;
	}
	public Date getUpdatedAt() {
		return updatedAt;
	}
	public void setUpdatedAt(Date updatedAt) {
		this.updatedAt = updatedAt;
	}
	public Appointment getAppointment() {
		return appointment;
	}
	public void setAppointment(Appointment appointment) {
		this.appointment = appointment;
	}

}

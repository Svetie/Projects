package com.newton.lookify.controllers;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.newton.lookify.models.Song;
import com.newton.lookify.services.LookifyService;

@Controller
public class LookifyController {
	private final LookifyService lookifyService;
	
	public LookifyController(LookifyService lookifyService) {
		this.lookifyService = lookifyService;
	}
	
	@RequestMapping("/")
	public String welcomePage() {
		return "welcome.jsp";
	}
	
	@RequestMapping("/dashboard")
	public String dashboardShow(Model model, @ModelAttribute("song") Song song) {
		List<Song> allSongs = this.lookifyService.allSongs();
		model.addAttribute("allSongs", allSongs);
		return "dashboard.jsp";
	}
	
	@RequestMapping("/songs/new")
	public String newSong(@ModelAttribute("song") Song song) {
		return "new.jsp";
	}
	
	@PostMapping("/new")
	public String createSong(@ModelAttribute("song") Song song, BindingResult result) {
        if (result.hasErrors()) {
            return "new.jsp";
        } else {
            lookifyService.createSong(song);
            return "redirect:/dashboard";
        }
	}
	
	@RequestMapping("/songs/{id}")
	public String showDetailsOfSong(@PathVariable("id") Long id, Model model) {
		Song song = this.lookifyService.findSongByID(id);
		model.addAttribute("song", song);
		return "show.jsp";
	}

	@RequestMapping("/delete/{id}")
	public String deleteASong(@PathVariable("id") Long id) {
		this.lookifyService.deleteSong(id);
		return "redirect:/dashboard";
	}
	
//	@RequestMapping("/search/{artist}")
//	public String findSongsOfArtist(@PathVariable("artist") String artist, 
//			@ModelAttribute("song") Song song, Model model) {
//		List<Song> allSongs = this.lookifyService.findByArtist(artist);
//		System.out.println(allSongs);
//		model.addAttribute("allSongs", allSongs);
//		return "artist.jsp";
//	}
//	
	
	@RequestMapping("/search")
	public String findSongsOfArtist(@ModelAttribute("song") Song song, Model model, 
			@RequestParam("artist") String artist) {
		model.addAttribute("artist", artist);
		List<Song> allSongs = this.lookifyService.findByArtist(artist);
		System.out.println(allSongs);
		model.addAttribute("allSongs", allSongs);
		return "artist.jsp";
	}
	
	@RequestMapping("/topten")
	public String topTenGet(Model model) {
		List<Song> songs = this.lookifyService.topTen();
		model.addAttribute("songs", songs);
		return "topten.jsp";
	}
}
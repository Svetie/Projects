package com.newton.lookify.services;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import com.newton.lookify.models.Song;
import com.newton.lookify.repositories.LookifyRepository;

@Service
public class LookifyService {
	
	private final LookifyRepository lookifyRepository;
	
	public LookifyService(LookifyRepository lookifyRepository) {
		this.lookifyRepository = lookifyRepository;
	}
	
	// get all songs
	public List<Song> allSongs() {
		return this.lookifyRepository.findAll();
	}
	
	// create a new song
	public Song createSong(Song song) {
		return this.lookifyRepository.save(song);
	}
	
	// find a song by its id
	public Song findSongByID(Long id) {
		Optional<Song> optionalSong = lookifyRepository.findById(id);
        if(optionalSong.isPresent()) {
            return optionalSong.get();
        } else {
            return null;
        }
	}
	
	// find song by the Artist's name
	public List<Song> findByArtist(String artist) {
		List<Song> songs = this.lookifyRepository.findByArtistContaining(artist);
		return songs;
	}
	
	public List<Song> topTen(){
		List<Song> songs = this.lookifyRepository.findTop10ByOrderByRatingDesc();
		return songs;
	}
	
	// delete song
	public void deleteSong(Long id) {
		this.lookifyRepository.deleteById(id);
	}
}

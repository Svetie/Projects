package com.newton.lookify.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.newton.lookify.models.Song;

@Repository
public interface LookifyRepository extends CrudRepository<Song, Long>{
    // this method retrieves all the books from the database
    List<Song> findAll();
    
    @Query("select song from Song song where song.artist like ?1")
    List<Song> findSongsByArtist(String artist);
    
    List<Song> findByArtistContaining(String artist);
//    List<Song> findByArtistIgnoreCase(String artist);
    
    List<Song> findTop10ByOrderByRatingDesc();
}

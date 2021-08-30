package com.newton.guzelSite.repositories;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import com.newton.guzelSite.models.BeautyService;

@Repository
public interface ServiceRepository extends CrudRepository<BeautyService, Long> {
	List<BeautyService> findAll();
}

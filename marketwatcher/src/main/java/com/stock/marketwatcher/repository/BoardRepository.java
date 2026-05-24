package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BoardRepository extends JpaRepository<Board,Long> {


}

package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.repository.search.BoardSearch;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface BoardRepository extends JpaRepository<Board,Long>, BoardSearch {
        @Query(value="select now()",nativeQuery = true)
            String getItem();

}

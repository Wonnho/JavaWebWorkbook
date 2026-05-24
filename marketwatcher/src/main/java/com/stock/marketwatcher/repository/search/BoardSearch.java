package com.stock.marketwatcher.repository.search;

import com.stock.marketwatcher.domain.Board;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface BoardSearch {
       Page<Board> search1(Pageable pageable);
}

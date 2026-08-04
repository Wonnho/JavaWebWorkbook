package com.stock.marketwatcher.repository.search;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.dto.BoardListReplyCountDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface BoardSearch {
       Page<Board> search1(Pageable pageable);
      Page<Board> searchAll(String[] types,String keyword,Pageable pageable);
       Page<BoardListReplyCountDTO> searchWithReplyCount(String[] types, String keyword, Pageable pageable);


        Page<BoardListReplyCountDTO>  searchWithAll(String[] types,String keyword,Pageable pageable);

}

package com.stock.marketwatcher.repository.search;

import com.querydsl.jpa.JPQLQuery;
import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.QBoard;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;

import java.util.List;

public class BoardSearchImpl extends QuerydslRepositorySupport implements BoardSearch {

    /**
     * Creates a new {@link QuerydslRepositorySupport} instance for the given domain type.
     *
     * @param domainClass must not be {@literal null}.
     */
    public BoardSearchImpl() {
        super(Board.class);
    }

    @Override
    public Page<Board> search1(Pageable pageable) {
        QBoard board=QBoard.board; //Q domain object

        JPQLQuery<Board> query=from(board);
        query.where(board.title.contains("1"));

        this.getQuerydsl().applyPagination(pageable,query);

        List<Board> list=query.fetch();

        long count=query.fetchCount();
        return null;
    }


}

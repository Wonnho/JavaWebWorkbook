package com.stock.marketwatcher.repository.search;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.jpa.JPQLQuery;
import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.QBoard;
import com.stock.marketwatcher.domain.QReply;
import com.stock.marketwatcher.dto.BoardListReplyCountDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
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
        //query.where(board.title.contains("1"));
        //this.getQuerydsl().applyPagination(pageable,query);

        BooleanBuilder booleanBuilder=new BooleanBuilder();
        booleanBuilder.or(board.title.contains("11"));
        booleanBuilder.or(board.content.contains("11"));
        query.where(booleanBuilder);
        query.where(board.bno.gt(0L));

        List<Board> list=query.fetch();

        long count=query.fetchCount();
        return null;
    }

    @Override
    public Page<Board> searchAll(String[] types, String keyword, Pageable pageable) {

        QBoard board=QBoard.board;
        JPQLQuery<Board> query=from(board);

        if( (types != null && types.length > 0) && keyword != null ){ //검색 조건과 키워드가 있다면

            BooleanBuilder booleanBuilder = new BooleanBuilder(); // (

            for(String type: types){

                switch (type){
                    case "t":
                        booleanBuilder.or(board.title.contains(keyword));
                        break;
                    case "c":
                        booleanBuilder.or(board.content.contains(keyword));
                        break;
                    case "w":
                        booleanBuilder.or(board.writer.contains(keyword));
                        break;
                }
            }//end for
            query.where(booleanBuilder);
        }//end if

        //bno > 0
        query.where(board.bno.gt(0L));

        //paging
        this.getQuerydsl().applyPagination(pageable, query);

        List<Board> list = query.fetch();

        long count = query.fetchCount();

        //return null;
        return new PageImpl<>(list, pageable, count);

    }

    @Override
    public Page<BoardListReplyCountDTO> searchWithReplyCount(String[] types,
                                                             String keyword, Pageable pageable) {

        QBoard board=QBoard.board;
        QReply reply=QReply.reply;
         JPQLQuery<Board> query=from(board);
         query.leftJoin(reply).on(reply.board.eq(board));
         query.groupBy(board);

        return null;
    }


}

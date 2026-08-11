package com.stock.marketwatcher.repository.search;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.Tuple;
import com.querydsl.core.types.Projections;
import com.querydsl.jpa.JPQLQuery;
import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.QBoard;
import com.stock.marketwatcher.domain.QReply;
import com.stock.marketwatcher.domain.QBoardImage;
import com.stock.marketwatcher.dto.BoardListAllDTO;
import com.stock.marketwatcher.dto.BoardListReplyCountDTO;
import com.stock.marketwatcher.dto.BoardImageDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.stream.Collectors;

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

        if( (types != null && types.length > 0) && keyword != null ){

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
        }

        //bno > 0
        query.where(board.bno.gt(0L));

        JPQLQuery<BoardListReplyCountDTO> dtoQuery=query.select(Projections.bean(BoardListReplyCountDTO.class,
                 board.bno,
                 board.title,
                 board.writer,
                 board.regDate,
                 reply.count().as("replyCount")
         ));

        this.getQuerydsl().applyPagination(pageable,dtoQuery);

        List<BoardListReplyCountDTO> dtoList = dtoQuery.fetch();

        long count = dtoQuery.fetchCount();

        return new PageImpl<>(dtoList, pageable, count);
    }

    @Override
    public Page<BoardListAllDTO> searchWithAll(String[] types, String keyword, Pageable pageable) {
        QBoard board = QBoard.board;
        QReply reply = QReply.reply;

        // 검색 조건
        BooleanBuilder where = new BooleanBuilder();
        if (types != null && types.length > 0 && keyword != null) {
            for (String type : types) {
                switch (type) {
                    case "t": where.or(board.title.contains(keyword)); break;
                    case "c": where.or(board.content.contains(keyword)); break;
                    case "w": where.or(board.writer.contains(keyword)); break;
                }
            }
        }

        // 1) 게시글 + 댓글수 : 엔티티를 튜플에 담지 않고 스칼라만 프로젝션 (Hibernate 6.6 회피)
        JPQLQuery<Board> query = from(board);
        query.leftJoin(reply).on(reply.board.eq(board));
        query.where(where);
        query.groupBy(board);

        JPQLQuery<BoardListAllDTO> dtoQuery = query.select(Projections.bean(BoardListAllDTO.class,
                board.bno,
                board.title,
                board.writer,
                board.regDate,
                reply.countDistinct().as("replyCount")));

        getQuerydsl().applyPagination(pageable, dtoQuery);

        List<BoardListAllDTO> dtoList = dtoQuery.fetch();

        // 2) 이미지 별도 조회 후 bno 기준으로 매핑
        List<Long> bnoList = dtoList.stream()
                .map(BoardListAllDTO::getBno)
                .collect(Collectors.toList());

        if (!bnoList.isEmpty()) {
            QBoardImage boardImage = QBoardImage.boardImage;
            List<Tuple> imageRows = from(boardImage)
                    .where(boardImage.board.bno.in(bnoList))
                    .orderBy(boardImage.board.bno.asc(), boardImage.ord.asc())
                    .select(boardImage.board.bno, boardImage.uuid, boardImage.fileName, boardImage.ord)
                    .fetch();

            Map<Long, List<BoardImageDTO>> imageMap = new HashMap<>();
            for (Tuple row : imageRows) {
                Long targetBno = row.get(boardImage.board.bno);
                Integer ord = row.get(boardImage.ord);
                BoardImageDTO imageDTO = BoardImageDTO.builder()
                        .uuid(row.get(boardImage.uuid))
                        .fileName(row.get(boardImage.fileName))
                        .ord(ord == null ? 0 : ord)
                        .build();
                imageMap.computeIfAbsent(targetBno, k -> new ArrayList<>()).add(imageDTO);
            }

            dtoList.forEach(dto ->
                    dto.setBoardImages(imageMap.getOrDefault(dto.getBno(), new ArrayList<>())));
        }

        // 3) 전체 개수
        Long totalCount = from(board).where(where).select(board.count()).fetchOne();

        return new PageImpl<>(dtoList, pageable, totalCount == null ? 0 : totalCount);
    }
}

package org.workbook.domain;

import lombok.*;

@NoArgsConstructor
@AllArgsConstructor
@Builder
@Getter
@ToString
public class MemberVO {
    private String todoid;
    private String todopw;
    private String todoname;

}

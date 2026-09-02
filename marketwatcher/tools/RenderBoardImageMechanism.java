import javax.imageio.ImageIO;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.RoundRectangle2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class RenderBoardImageMechanism {
    private static final int WIDTH = 1500;
    private static final int HEIGHT = 980;
    private static final Color BG = new Color(248, 250, 252);
    private static final Color CARD = Color.WHITE;
    private static final Color BORDER = new Color(203, 213, 225);
    private static final Color TEXT = new Color(15, 23, 42);
    private static final Color MUTED = new Color(71, 85, 105);
    private static final Color BLUE = new Color(37, 99, 235);
    private static final Color GREEN = new Color(22, 163, 74);
    private static final Color PURPLE = new Color(124, 58, 237);

    record Box(String title, String body, int x, int y, int w, int h, Color accent) {}

    public static void main(String[] args) throws Exception {
        File output = new File(args.length > 0 ? args[0] : "docs/board-image-mechanism.png");
        File parent = output.getParentFile();
        if (parent != null) {
            parent.mkdirs();
        }

        BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        g.setColor(BG);
        g.fillRect(0, 0, WIDTH, HEIGHT);

        g.setFont(new Font("Arial", Font.BOLD, 34));
        g.setColor(TEXT);
        g.drawString("Board Image Register Mechanism", 70, 72);

        g.setFont(new Font("Arial", Font.PLAIN, 18));
        g.setColor(MUTED);
        g.drawString("How BoardDTO fileNames become BoardImage rows through dtoToEntity(), addImage(), and JPA cascade.", 70, 108);

        List<Box> boxes = new ArrayList<>();
        boxes.add(new Box("BoardDTO", "title, content, writer\nfileNames: uuid_aaa.jpg...", 80, 180, 260, 130, BLUE));
        boxes.add(new Box("BoardService.register()", "Receives the DTO from test\nor controller", 430, 180, 260, 130, BLUE));
        boxes.add(new Box("dtoToEntity()", "Builds Board entity\nfrom BoardDTO fields", 780, 180, 260, 130, BLUE));
        boxes.add(new Box("Board Entity", "bno, title, content, writer\nimageSet = HashSet", 1130, 180, 260, 130, GREEN));

        boxes.add(new Box("Loop fileNames", "For each uploaded/saved\nfile name", 430, 420, 260, 130, PURPLE));
        boxes.add(new Box("split(\"_\", 2)", "uuid_aaa.jpg becomes\nuuid + aaa.jpg", 780, 420, 260, 130, PURPLE));
        boxes.add(new Box("board.addImage()", "Creates BoardImage and\nconnects it to Board", 1130, 420, 260, 130, PURPLE));

        boxes.add(new Box("BoardImage Entity", "uuid, fileName, ord\nboard = parent Board", 780, 670, 260, 130, GREEN));
        boxes.add(new Box("boardRepository.save(board)", "One save call on Board", 430, 670, 260, 130, BLUE));
        boxes.add(new Box("Hibernate SQL", "insert board\ninsert board_image x3", 80, 670, 260, 130, GREEN));

        drawLane(g, 52, 145, 1398, 700);

        for (Box box : boxes) {
            drawBox(g, box);
        }

        drawArrow(g, 340, 245, 430, 245, BLUE);
        drawArrow(g, 690, 245, 780, 245, BLUE);
        drawArrow(g, 1040, 245, 1130, 245, BLUE);

        drawArrow(g, 910, 310, 560, 420, PURPLE);
        drawArrow(g, 690, 485, 780, 485, PURPLE);
        drawArrow(g, 1040, 485, 1130, 485, PURPLE);
        drawArrow(g, 1260, 550, 910, 670, PURPLE);

        drawArrow(g, 780, 735, 690, 735, BLUE);
        drawArrow(g, 430, 735, 340, 735, GREEN);

        drawNote(g, 80, 865, "Result in your test log: 1 row inserted into board, then 3 rows inserted into board_image because Board.imageSet uses cascade = CascadeType.ALL.");

        g.dispose();
        ImageIO.write(image, "png", output);
        System.out.println(output.getAbsolutePath());
    }

    private static void drawLane(Graphics2D g, int x, int y, int w, int h) {
        g.setColor(new Color(241, 245, 249));
        g.fillRoundRect(x, y, w, h, 24, 24);
        g.setColor(new Color(226, 232, 240));
        g.setStroke(new BasicStroke(2));
        g.drawRoundRect(x, y, w, h, 24, 24);
    }

    private static void drawBox(Graphics2D g, Box box) {
        g.setColor(new Color(15, 23, 42, 18));
        g.fillRoundRect(box.x + 6, box.y + 8, box.w, box.h, 18, 18);
        g.setColor(CARD);
        g.fill(new RoundRectangle2D.Double(box.x, box.y, box.w, box.h, 18, 18));
        g.setColor(BORDER);
        g.setStroke(new BasicStroke(2));
        g.drawRoundRect(box.x, box.y, box.w, box.h, 18, 18);
        g.setColor(box.accent);
        g.fillRoundRect(box.x, box.y, 10, box.h, 18, 18);

        g.setFont(new Font("Arial", Font.BOLD, 22));
        g.setColor(TEXT);
        g.drawString(box.title, box.x + 28, box.y + 38);

        g.setFont(new Font("Arial", Font.PLAIN, 17));
        g.setColor(MUTED);
        int lineY = box.y + 72;
        for (String line : box.body.split("\\n")) {
            g.drawString(line, box.x + 28, lineY);
            lineY += 26;
        }
    }

    private static void drawArrow(Graphics2D g, int x1, int y1, int x2, int y2, Color color) {
        g.setColor(color);
        g.setStroke(new BasicStroke(3, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g.drawLine(x1, y1, x2, y2);
        double angle = Math.atan2(y2 - y1, x2 - x1);
        int len = 14;
        int xA = (int) (x2 - len * Math.cos(angle - Math.PI / 6));
        int yA = (int) (y2 - len * Math.sin(angle - Math.PI / 6));
        int xB = (int) (x2 - len * Math.cos(angle + Math.PI / 6));
        int yB = (int) (y2 - len * Math.sin(angle + Math.PI / 6));
        g.drawLine(x2, y2, xA, yA);
        g.drawLine(x2, y2, xB, yB);
    }

    private static void drawNote(Graphics2D g, int x, int y, String text) {
        g.setColor(new Color(239, 246, 255));
        g.fillRoundRect(x, y, 1320, 58, 16, 16);
        g.setColor(new Color(191, 219, 254));
        g.setStroke(new BasicStroke(2));
        g.drawRoundRect(x, y, 1320, 58, 16, 16);

        g.setFont(new Font("Arial", Font.PLAIN, 18));
        g.setColor(TEXT);
        FontMetrics metrics = g.getFontMetrics();
        int textY = y + ((58 - metrics.getHeight()) / 2) + metrics.getAscent();
        g.drawString(text, x + 22, textY);
    }
}

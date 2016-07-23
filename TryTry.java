import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by avanish on 15/7/16.
 */
public class TryTry {

    public static void main(String[] args)  throws Exception {
        BufferedReader br = new BufferedReader(new FileReader("trytry.txt"));
        List <String> list = new ArrayList <String> ();
        String s;
        while((s = br.readLine()) != null) {
            if(s.equals("")) {
                continue;
            }
            list.add(s);
        }
        Connection connection = null;

        try {
            try {
                connection = DatabaseConnection.getConnection();
            } catch (Exception e) {
                e.printStackTrace();
            }

            int count = 0;
            Statement statement = connection.createStatement();
            for (int i = 0; i < list.size(); i++) {
                String text = list.get(i);
                //text = text.replaceAll("[~`!@#$%^&*()_+-=0-9{}\\|;:\'\",<.>/?]+", "");
                System.out.println(text);
                String query = "insert into textDescription (textID, text) values ('" + i + "', '" + text + "');";
                statement.executeUpdate(query);
                String[] tokens = text.split("\\s+");
                for (int j = 0; j < tokens.length; j++) {
                    System.out.println(tokens[j]);
                    query = "insert into invertedIndex (id, keyword, textID) values ('" + count + "', '" + tokens[j] + "', '" + i + "');";
                    statement.executeUpdate(query);
                    count++;
                }
            }
        }
        catch(SQLException e) {
            e.printStackTrace();
        }

    }
}

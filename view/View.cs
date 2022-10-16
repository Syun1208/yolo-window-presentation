using System;
using System.Drawing;
using System.IO;
using System.Net;
using System.Text;
using System.Data;
using System.Collections.Generic
using System.Linq
using System.Threading.Tasks
using MySql.Data.MySqlClient;
using MySql.Data;

namespace AdvancedTopicInCE.view
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        // Ham goi HTTP Get len server
        public string SendGet(string uri)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;

            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (Stream stream = response.GetResponseStream())
                if (stream != null)
                    using (StreamReader reader = new StreamReader(stream))
                    {
                        return reader.ReadToEnd();
                    }
        }

        // Ham chuyen Image thanh Base 64
        public static string ConvertImageToBase64String(Image image)
        {
            using (MemoryStream ms = new MemoryStream())
            {
               
                image.Save(ms, System.Drawing.Imaging.ImageFormat.Bmp);
                return Convert.ToBase64String(ms.ToArray());
            }
        }

        // Ham convert B64 de gui len server
        private String EscapeData(String b64)
        {
            int b64Length = b64.Length;
            if (b64Length <= 32000)
            {
                return Uri.EscapeDataString(b64);
            }


            int idx = 0;
            StringBuilder builder = new StringBuilder();
            String substr = b64.Substring(idx, 32000);
            while (idx < b64Length)
            {
                builder.Append(Uri.EscapeDataString(substr));
                idx += 32000;

                if (idx < b64Length)
                {

                    substr = b64.Substring(idx, Math.Min(32000, b64Length - idx));
                }

            }
            return builder.ToString();

        }

        // Ham goi HTTP POST len server de detect
        private String SendPost(String url, String b64)
        {
            try
            {
                var request = (HttpWebRequest)WebRequest.Create(url);
                request.Timeout = 5000;
                var postData = "image=" + EscapeData(b64);

                var data = Encoding.ASCII.GetBytes(postData);

                request.Method = "POST";
                request.ContentType = "application/x-www-form-urlencoded";
                request.ContentLength = data.Length;

                using (var stream = request.GetRequestStream())
                {
                    stream.Write(data, 0, data.Length);
                }

                var response = (HttpWebResponse)request.GetResponse();

                var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();

                return responseString;
            }
            catch (Exception ex)
            {
                return "Exception" + ex.ToString();
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Doc du lieu cac ten class tu file yolov3.txt 
            string[] lines = File.ReadAllLines("yolov5.txt");

            // Convert image to B64
            String b64 = ConvertImageToBase64String(pictureBox1.Image);
           
            // Goi len server va tra ve ket qua
            const string serverIp = "192.168.8.123";
            const string serverPath = "http://" + serverIp + ":8000/id-card-yolo/detect/";
            String retStr = SendPost(serverPath, b64);

           
            // Ve cac khung chu nhat va ten class len anh 
            Graphics newGraphics = Graphics.FromImage(pictureBox1.Image);

            String[] items = retStr.Split('|');
            for (int idx=0;idx<items.Length-1;idx++)
            {
                String[] val = items[idx].Split(',');
                // Draw it
                Pen blackPen = new Pen(Color.Black, 2);

                // Create rectangle.
                Rectangle rect = new Rectangle(int.Parse(val[1]), int.Parse(val[2]), int.Parse(val[3]), int.Parse(val[4]));

                // Draw rectangle to screen.
                newGraphics.DrawRectangle(blackPen, rect);
                newGraphics.DrawString(lines[int.Parse(val[0])], new Font("Tahoma", 8), Brushes.Black, rect);

            }

            pictureBox1.Refresh();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Resize anh cua picture box 1 de dam bao dung scale
            Image image = (Image)(new Bitmap(pictureBox1.Image, new Size(pictureBox1.Width, pictureBox1.Height)));
            pictureBox1.Image = image;
        }
    }
     class DBConnection {
        public MySqlConnection dbc = null;
        public string Connection() {
            string connectString = string.Format(@"server = localhost;
                                                   user = root;
                                                   password = ***;
                                                   database = stardb");
            dbc = new MySqlConnection(connectString);
            MySqlConnection connection = new MySqlConnection(connectString);
            try {
                connection.Open();
            }
            catch(Exception ex) {
                return ex.ToString();
            }
            return null;
        }

        public void ConnectionClose() {
            dbc.Close();
        }
        public DataSet Starcraft() {

            MySqlDataAdapter adapter;
            string query = "select * from unit";
            adapter = new MySqlDataAdapter(query, dbc);

            DataSet data = new DataSet();
            adapter.Fill(data, "unit");

            return data;
        }
        public void InsertObjectInfor(){
            dbc.Open();
            for (int idx=0;idx<items.Length-1;idx++)
            {
                String[] val = items[idx].Split(',');
                string Class = val[0];
                float xmin = float.Parse(val[1]);
                float ymin = float.Parse(val[2]);
                float xmax = float.Parse(val[3]);
                float ymax = float.Parse(val[4]);
                string query = 'INSERT INTO user_table VALUES (@stringClass, @floatxmin, @floatymin, @floatxmax, @floatymax)';
                MySqlCommand cmd = new MySqlCommand(query, dbc);
                cmd.CommandType = CommandType.Text; 
                cmd.Parameters.Add('@stringClass', MySqlDbType.VarChar).Value = Class;
                cmd.Parameters.Add('@stringxmin', MySqlDbType.VarChar).Value = xmin;
                cmd.Parameters.Add('@stringymin', MySqlDbType.VarChar).Value = ymin;
                cmd.Parameters.Add('@stringxmax', MySqlDbType.VarChar).Value = xmax;
                cmd.Parameters.Add('@stringymax', MySqlDbType.VarChar).Value = ymax;
            }
        
            try{
                cmd.ExecuteNonQuery();
                MessageBox.Show("Added Successfully.", 'Information', MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (MySqlException ex){
                MessageBox.Show("Failed. \n", ex.Message, MessageBoxButtons.OK, MessageBoxIcon.Error);

            }
        }
        // public void InsertData() {
        //     dbc.Open();
        //     string query = "insert into unit values (null, '테란', '사이클론', 20, 0)";
        //     MySqlCommand cmd = new MySqlCommand(query, dbc);
        //     cmd.ExecuteNonQuery();
        // }
        public void DeleteSomeInference(string Class){
            dbc.Open();
            string query = 'DELETE FROM user_table WHERE Class =  @stringClass';
            MySqlCommand cmd = new MySqlCommand(query, dbc);
            cmd.CommandType = CommandType.Text; 
            cmd.Parameters.Add('@stringClass', MySqlDbType.VarChar).Value = Class;
            try{
                cmd.ExecuteNonQuery();
                MessageBox.Show("Deleted Successfully.", 'Information', MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (MySqlException ex){
                MessageBox.Show("Failed. \n", ex.Message, MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        public static void DisplayAndSearch(string query, DataGridView dgv){
            dbs.Open();
            MySqlCommand cmd = new MySqlCommand(query, dbc);
            MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
            DataTable datatable = new DataTable();
            adapter.Fill(datatable);

        }
        // public void DeleteData() {
        //     dbc.Open();
        //     try{
        //         string query = "delete from unit where name = '사이클론'";
        //         MySqlCommand cmd = new MySqlCommand(query, dbc);
        //         cmd.ExecuteNonQuery();
        //     } catch(Exception ex) {
        //         Console.WriteLine(ex);
        //     }
        // }
    }
}
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Web;
using System.Net;
using System.IO;


namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.label1.Text = YouDaoTranslateTool(this.textBox1.Text.ToString());
        }
        public static string YouDaoTranslateTool(string sourceWord)
        {
            StreamReader reader = new StreamReader(@"D:\word\raw.txt");
            StreamWriter sw = new StreamWriter(@"e:\1.txt", true);
            int i = 0;
           while(i<=3)
            {
                sourceWord = reader.ReadLine();


                /*
                调用：http://fanyi.youdao.com/openapi.do?keyfrom=sasfasdfasf&key=1177596287&type=data&doctype=json&version=1.1&q=中国人
                返回的json格式如下：
                {"translation":["The Chinese"],"basic":{"phonetic":"zhōng guó rén","explains":["Chinese","Chinaman","Chinese people","Chinee","chow"]}
                 * ,"query":"中国人","errorCode":0,"web":[{"value":["Chinaren","Chinese people","The Chinese","Chinese person"],"key":"中国人"},
                 * {"value":["中国人"],"key":"中國人"},{"value":["CHINA LIFE","LFC","china life insurance","YZC"],"key":"中国人寿"},{"value":["Human Rights in China","HRIC"],"key":"中国人权"},
                 * {"value":["China Life Insurance Company","China Life Insurance","China Life","China Life Insurance Co Ltd"],"key":"中国人寿保险"},
                 * {"value":["Chinese name","Chinese Names in English","Courtesy Name"],"key":"中国人名"},{"value":["Chinese Names"],"key":"中国人的名字"},
                 * {"value":["CJOL"],"key":"中国人才热线"},{"value":["American Born Chinese"],"key":"美生中国人"},{"value":["Chinese Characteristics"],"key":"中国人德行"}]}*/
                string serverUrl = @"http://fanyi.youdao.com/openapi.do?keyfrom=sasfasdfasf&key=1177596287&type=data&doctype=json&version=1.1&q="
                + HttpUtility.UrlEncode(sourceWord);
                WebRequest request = WebRequest.Create(serverUrl);
                WebResponse response = request.GetResponse();
                string resJson = new StreamReader(response.GetResponseStream(), Encoding.UTF8).ReadToEnd();
                int textIndex = resJson.IndexOf("translation") + 15;
                int textLen = resJson.IndexOf("\"]", textIndex) - textIndex;
                //   return resJson.Substring(textIndex, textLen);
                //File.WriteAllText(@"e:\1.txt", resJson);

                i++;
                sw.Write(resJson + "\r\n");
            }
                sw.Close();
                string resJson1 = "abc";
        
            return resJson1;
        }
    }
}

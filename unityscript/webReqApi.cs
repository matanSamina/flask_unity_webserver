using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;


public class webReqApi : MonoBehaviour
{
    public string FileName = "file name here";
    private string PathToFile;

    void Start()
    {
        PathToFile = Application.streamingAssetsPath + "/" + FileName;
        StartCoroutine(GetRequest("http://127.0.0.1:5000/unity", PathToFile));
    }

    IEnumerator GetRequest(string uri, string path)
    {

        UnityWebRequest dataFile = UnityWebRequest.Get(path);
        yield return dataFile.SendWebRequest();

        WWWForm form = new WWWForm();

        form.AddField("name", "nameOfSubject");
        form.AddField("frameCount", Time.frameCount.ToString());
        form.AddBinaryData("dataFile", dataFile.downloadHandler.data, Path.GetFileName(path));

        using (UnityWebRequest www = UnityWebRequest.Post(uri, form))
        {
            yield return www.SendWebRequest();
            Debug.Log("SERVER: " + www.downloadHandler.text); // server response

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log("Form upload completed!");
            }
        }
    }
}
$url = "http://127.0.0.1:13579"

while ($true) {
    try {
        $request = [System.Net.HttpWebRequest]::Create($url)
        $request.Method = "HEAD"
        $request.Timeout = 5000
        $response = $request.GetResponse()
    } catch [System.Net.WebException] {
        $statusCode = [int]$_.Exception.Response.StatusCode
        
        if ($statusCode -eq 200 -or ($statusCode -ge 400 -and $statusCode -le 405)) {
            Write-Host "Qsign API ״̬����."
        } else {
            Write-Host "��⵽Qsign API�����ߣ�������������..."
            
            # ������Ŀ(�����滻�����Լ��������ű����ݷ�ʽ·��)
            Start "Start_Qsign.bat"
            
            Write-Host "Qsign�������������"
        }
    }
    
    # �ȴ�һ��ʱ���������
    Start-Sleep -Seconds 30
}

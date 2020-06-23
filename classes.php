<?php

class FileReader {
	private $fileOpen;
	private $position;
	public $countLogs;
	
	function __construct() {
		$this->fileOpen = fopen('dism.log', 'r');
		$this->position = -2;
        if (isset($_POST['count-logs']) && $_POST['count-logs']) {
            $this->count = $_POST['count-logs'];
        } else {
            $this->count = 50;
        }
	}
	
	function close() {
		if($this->fileOpen) {
			fclose($this->fileOpen);
		}
	}
	
	function readBack() {
		if($this->fileOpen) {
			if($this->position == -2) {
				$stat = fstat($this->fileOpen);
				$this->position = $stat['size'] - 1;
			}
			
			$log = '';
			for(; $this->position >= 0; $this->position--) {
				fseek($this->fileOpen, $this->position);
				$char = fgetc($this->fileOpen);
				$log = $char.$log;
				if($char == "\n") { 
					$this->position--;
					break;
				}
			}
			return $log;
		}
	}
	
	function feofBack() {
		return $this->position != -1;
	}

    function getLogs() {
        $logs = [];
        for ($i = 0; $i < $this->count && $this->feofBack() == true; $i++) {
            $logs[] = $this->readBack();
        }
        return $logs;
    }
};

class WorkWithLogs {
    private $parsedLoges;
    private $file;
    public $logs;

    function __construct() {
        $this->file = new FileReader();
        $this->logs = $this->file->getLogs();
        $this->parsedLoges = $this->parseLogs($this->logs);
        $this->filter();
    }

    function filter() {
        if (isset($_POST['type-message']) && $_POST['type-message']) {
            $this->logs = $this->filterByTypeMessage($_POST['type-message']);
        }
        if ((isset($_POST['start-period']) && $_POST['start-period']) || (isset($_POST['end-period']) && $_POST['end-period'])) {
            $this->logs = $this->filterByPeriod($_POST['start-period'], $_POST['end-period']);
        }
        if (isset($_POST['count-logs']) && $_POST['count-logs']) {
            $this->logs = $this->filterByCount($_POST['count-logs']);
        }
        if (isset($_POST['search']) && $_POST['search']) {
            $this->logs = $this->filterBySearch($_POST['search']);
        }
    }

    function filterByCount($countLogs) {
        return array_slice($this->logs, 0, $countLogs);
    }

    function filterBySearch($text) {
        $filteredLogs = [];
        foreach ($this->logs as $key => $log) {
            if (stripos($log, $text)) {
                $filteredLogs[] = $log;
            }
        }
        return $filteredLogs;
    }

    function filterByTypeMessage($typeMessage) {
        $filteredLogs = [];
        foreach ($this->logs as $key => $log) {
            if ($this->parsedLoges[$key]['MESSAGE_TYPE'] == $typeMessage) {
                $filteredLogs[] = $log;
            }
        }
        return $filteredLogs;
    }

    function filterByPeriod($start, $end) {
        $filteredLogs = [];
        foreach ($this->logs as $key => $log) {
            $timestamp = date('Y-m-d', strtotime($this->parsedLoges[$key]['TIMESTAMP']));
            if (!empty($start)) {
                if (!empty($end) && ($timestamp <= date($end)) && ($timestamp >= date($start))) {
                    $filteredLogs[] = $log;
                } elseif (empty($end) && $timestamp >= date($start)) {
                    $filteredLogs[] = $log;
                }
            } elseif (!empty($end) && ($timestamp <= date($end))) {
                $filteredLogs[] = $log;
            }
        }
        return $filteredLogs;
    }

    function parseLogs($arrayLogs) {
        $array = [];
        foreach ($arrayLogs as $key => $log) {
            $parsedLogs = [];
            $endDatetime = strpos($log, ',');
            $timestamp = substr($log, 0, $endDatetime);
            $log = str_replace($timestamp . ', ', '', $log);
            $messageType = substr($log, 0, strpos($log, ' '));
            $log = str_replace($messageType . ' ', '', $log);
            $sourceOfMessage = trim(substr($log, 0, strpos($log, ':')));
            $logMessageItself = trim(substr($log, strpos($log, ':') + 2));
            $array[$key] = [
                'TIMESTAMP' => $timestamp,
                'MESSAGE_TYPE' => $messageType,
                'SOURCE_OF_MESSAGE' => $sourceOfMessage,
                'LOG_MESSAGE_ITSELF' =>$logMessageItself
            ];
        }
        return $array;
    }
}

?>
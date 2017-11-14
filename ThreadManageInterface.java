package cn.com.hoonsoft.restv1;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import javax.inject.Singleton;
import javax.ws.rs.Consumes;
import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import cn.com.hoonsoft.ais.ControlAis;
import cn.com.hoonsoft.base.BaseControl;
import cn.com.hoonsoft.dto.DTO;
import cn.com.hoonsoft.dto.DTOCollection;
import cn.com.hoonsoft.enavrule.navigationrule.ControlJudge;
import cn.com.hoonsoft.enavrule.navigationrule.ControlSubscribe;
import cn.com.hoonsoft.kernel.KernelThreadDB;
import cn.com.hoonsoft.plan.ControlThreadContent;
import cn.com.hoonsoft.restinterfaceprocess.RestTool;
import cn.com.hoonsoft.tool.ExceptionRunningOperateToolFail;
import cn.com.hoonsoft.tool.ToolClient;
import cn.com.hoonsoft.tool.ToolLog;
import cn.com.hoonsoft.tool.ToolProperty;
import cn.com.hoonsoft.tool.ToolXML;

@Path("ThreadManager")
@Singleton
public class ThreadManageInterface extends BaseRestControl {

	public ThreadManageInterface() {
		this.setThreadDB(new KernelThreadDB());
	}
	public static int START_SUCCESS=200;//启动成功
	public static int RESTART_SUCCESS=201;//启动成功
	public static int SHUTDOWN_SUCCESS=211;//关闭成功
	public static int FAIL=400;//启动失败
	public static int ERROR=401;//参数错误
	public static int STATE_OPEN=303;//状态为开启
	public static int STATE_CLOSE=304;//状态为关闭
	
	@GET
	@Produces("text/plain")
	@Path("startRun")
	// 船位实时定位
	public Response startRunThread(@QueryParam("className") String className,
			@QueryParam("sleepTime") String sleepTime) {
		try {

			if ("true".equals(ToolProperty.gainPlanValue("ThreadControlEnable"))) {
				ScheduledExecutorService service = ThreadMap.get(className);
				ToolLog.warn("准备启动"+className, this.getClass());
				if (service == null) {
					service = Executors.newScheduledThreadPool(1);
					Runnable runnable = (Runnable) Class.forName(className).newInstance();
					service.scheduleAtFixedRate(runnable, 1, Integer.valueOf(sleepTime), TimeUnit.SECONDS);
					ThreadMap.put(className,service);
					return Response.status(START_SUCCESS).entity("start success").type(MediaType.TEXT_PLAIN).build();
					
				}else{
					service.shutdown();
					service = Executors.newScheduledThreadPool(1);
					Runnable runnable = (Runnable) Class.forName(className).newInstance();
					service.scheduleAtFixedRate(runnable, 1, Integer.valueOf(sleepTime), TimeUnit.SECONDS);
					ThreadMap.put(className,service);
					return Response.status(RESTART_SUCCESS).entity("restart success").type(MediaType.TEXT_PLAIN).build();
				}
				
			}
			
		} catch (Exception e) {
			return Response.status(FAIL).entity("fail").type(MediaType.TEXT_PLAIN).build();

		}
		return Response.status(ERROR).entity("error").type(MediaType.TEXT_PLAIN).build();

	}
	
	@GET
	@Produces("text/plain")
	@Path("queryState")
	//查询线程状态
	public Response queryState(@QueryParam("className") String className) {
		try {

			if ("true".equals(ToolProperty.gainPlanValue("ThreadControlEnable"))) {
				ScheduledExecutorService service = ThreadMap.get(className);
				if(service==null){
					return Response.status(STATE_CLOSE).entity("close").type(MediaType.TEXT_PLAIN).build();
				}else{
					return Response.status(STATE_OPEN).entity("open").type(MediaType.TEXT_PLAIN).build();
				}
				
			}
			
		} catch (Exception e) {
			return Response.status(FAIL).entity("fail").type(MediaType.TEXT_PLAIN).build();

		}
		return Response.status(ERROR).entity("error").type(MediaType.TEXT_PLAIN).build();

	}

	@GET
	@Produces("text/plain")
	@Path("shutDown")
	//关闭线程
	public Response shutDown(@QueryParam("className") String className) {
		try {

			if ("true".equals(ToolProperty.gainPlanValue("ThreadControlEnable"))) {
				ScheduledExecutorService service = ThreadMap.get(className);
				if(service==null){
					return Response.status(STATE_CLOSE).entity("close").type(MediaType.TEXT_PLAIN).build();
				}else{
					service.shutdown();
					ThreadMap.put(className, null);
					return Response.status(STATE_CLOSE).entity("close").type(MediaType.TEXT_PLAIN).build();
				}
				
			}
			
		} catch (Exception e) {
			return Response.status(FAIL).entity("fail").type(MediaType.TEXT_PLAIN).build();

		}
		return Response.status(ERROR).entity("error").type(MediaType.TEXT_PLAIN).build();

	}
	
	private static HashMap<String, ScheduledExecutorService> ThreadMap = new HashMap<>();

}

extern struct rtpkt {
    int sourceid;       /* id of sending router sending this pkt */
    int destid;         /* id of router to which pkt being sent 
                           (must be an immediate neighbor) */
    int mincost[4];    /* min cost to node 0 ... 3 */
};

void init_disttable(int selfid, int *disttable, int *mincost);
void updateneighbors(int selfid, int *mincost, int *disttable);
int updatecosts(struct rtpkt *rcvdpkt, int selfid, int *mincost, int *disttable);
void linkhandler(int linkid, int newcost, int selfid, int *mincost, int *disttable);

extern const int NODECOUNT; // number of total nodes in graph
extern const int INFINITY; // convention